import json
import hashlib
import logging
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import sys
import os
import asyncio

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from relevance_filtering.pipeline import RelevancePipeline

app = FastAPI(
    title="Semantic Relevance Filtering API",
    description="AI-powered API to filter brand mentions based on business relevance.",
    version="1.0.0"
)

# Allow the frontend to make requests to the API without CORS blocking
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Optional Redis Caching Setup
redis_client = None
CACHE_EXPIRATION = 86400  # 24 hours

try:
    import redis
    try:
        redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)
        redis_client.ping()
        logging.info("Connected to Redis for caching.")
    except Exception as e:
        logging.warning(f"Redis connection failed: {e}. Caching disabled.")
        redis_client = None
except ImportError:
    logging.warning("Redis package not found (`pip install redis`). Caching disabled.")

# Initialize the model globally so it stays warm in memory
relevance_filter = RelevancePipeline()

# PostgreSQL Integration
try:
    from . import database
    from sqlalchemy.orm import Session
    database.Base.metadata.create_all(bind=database.engine)
    
    def get_db():
        db = database.SessionLocal()
        try:
            yield db
        finally:
            db.close()
except ImportError:
    logging.warning("Database module not found. PostgreSQL integration disabled.")
    def get_db(): return None
except Exception as e:
    logging.warning(f"Database connection failed: {e}. PostgreSQL integration disabled.")
    def get_db(): yield None

# Real-Time Analytics WebSocket Manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                pass

manager = ConnectionManager()

def get_cache_key(text: str) -> str:
    """Generates a unique SHA-256 hash for the text to use as a Redis key."""
    text_hash = hashlib.sha256(text.encode('utf-8')).hexdigest()
    return f"relevance_cache:{text_hash}"

class TextRequest(BaseModel):
    text: str

class BatchTextRequest(BaseModel):
    texts: List[str]

class RelevanceResponse(BaseModel):
    post: str
    relevance_score: float
    matched_category: str
    confidence: str
    decision: str

class SemanticSearchRequest(BaseModel):
    query: str
    corpus: List[str] = []
    top_k: int = 5

class SemanticSearchResult(BaseModel):
    text: str
    score: float

@app.websocket("/ws/analytics")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()  # Keep connection open
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.post("/analyze/relevance", response_model=RelevanceResponse)
async def analyze_relevance(request: TextRequest, db: Session = Depends(get_db)):
    try:
        # 1. Check Cache
        if redis_client:
            cache_key = get_cache_key(request.text)
            cached = redis_client.get(cache_key)
            if cached:
                return RelevanceResponse(**json.loads(cached))
                
        # 2. Process via AI Model
        result = relevance_filter.evaluate_relevance(request.text)
        
        # 3. Save to PostgreSQL
        if db:
            db_mention = database.Mention(
                text=request.text,
                relevance_score=result["relevance_score"],
                matched_category=result["matched_category"],
                confidence=result["confidence"],
                decision=result["decision"]
            )
            db.add(db_mention)
            db.commit()

        # 4. Broadcast to Real-Time Analytics Dashboard
        await manager.broadcast(json.dumps(result))
        
        # 5. Save to Cache
        if redis_client:
            redis_client.setex(cache_key, CACHE_EXPIRATION, json.dumps(result))
            
        return RelevanceResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze/relevance/batch", response_model=List[RelevanceResponse])
async def analyze_relevance_batch(request: BatchTextRequest):
    try:
        texts = request.texts
        final_results = [None] * len(texts)
        texts_to_process = []
        indices_to_process = []
        
        # 1. Check Cache (Bulk)
        if redis_client and texts:
            cache_keys = [get_cache_key(t) for t in texts]
            cached_values = redis_client.mget(cache_keys)
            
            for i, (text, cached) in enumerate(zip(texts, cached_values)):
                if cached:
                    final_results[i] = RelevanceResponse(**json.loads(cached))
                else:
                    texts_to_process.append(text)
                    indices_to_process.append(i)
        else:
            texts_to_process = texts
            indices_to_process = list(range(len(texts)))

        # 2. Process Missing Items
        if texts_to_process:
            new_results = relevance_filter.process_batch(texts_to_process)
            
            for i, text, result in zip(indices_to_process, texts_to_process, new_results):
                final_results[i] = RelevanceResponse(**result)
                
                # 3. Save Misses to Cache
                if redis_client:
                    cache_key = get_cache_key(text)
                    redis_client.setex(cache_key, CACHE_EXPIRATION, json.dumps(result))
                    
        return final_results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search/semantic", response_model=List[SemanticSearchResult])
async def semantic_search(request: SemanticSearchRequest):
    try:
        corpus = request.corpus
        
        # If no corpus is provided, dynamically use Redis cache as the database
        if not corpus:
            if not redis_client:
                raise HTTPException(status_code=400, detail="No corpus provided and Redis is disabled.")
            
            keys = redis_client.keys("relevance_cache:*")
            if not keys:
                raise HTTPException(status_code=404, detail="Redis cache is empty. Please provide a corpus or analyze some texts first.")
                
            cached_values = redis_client.mget(keys)
            for cached in cached_values:
                if cached:
                    data = json.loads(cached)
                    if "post" in data:
                        corpus.append(data["post"])
                        
        results = relevance_filter.semantic_search(request.query, corpus, request.top_k)
        return results
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))