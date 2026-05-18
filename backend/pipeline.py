import numpy as np
from typing import List, Dict, Any
from .embedding_engine import EmbeddingEngine
from .similarity_engine import SimilarityEngine
from .category_manager import CategoryManager
from .threshold_manager import ThresholdManager

class RelevancePipeline:
    """
    Modular Relevance Pipeline handling semantic similarity, noise filtering, and threshold classification.
    """
    def __init__(self, model_name: str = 'BAAI/bge-large-en-v1.5'):
        self.embedding_engine = EmbeddingEngine(model_name)
        self.similarity_engine = SimilarityEngine()
        
        self.relevant_topics = CategoryManager.get_relevant_topics()
        self.noise_topics = CategoryManager.get_noise_topics()
        
        self.relevant_embeddings = self.embedding_engine.encode(self.relevant_topics)
        self.noise_embeddings = self.embedding_engine.encode(self.noise_topics)

    def evaluate_relevance(self, text: str) -> Dict[str, any]:
        if not text or not isinstance(text, str):
            return {
                "post": text if text else "",
                "relevance_score": 0.0,
                "matched_category": "None",
                "confidence": "0%",
                "decision": "Ignore"
            }
        return self.process_batch([text])[0]

    def process_batch(self, texts: List[str]) -> List[Dict[str, any]]:
        if not texts:
            return []
            
        text_embs = self.embedding_engine.encode(texts)
        sim_relevant = self.similarity_engine.calculate_similarity(text_embs, self.relevant_embeddings)
        sim_noise = self.similarity_engine.calculate_similarity(text_embs, self.noise_embeddings)
        
        max_rel_scores = np.max(sim_relevant, axis=1)
        best_rel_indices = np.argmax(sim_relevant, axis=1)
        max_noise_scores = np.max(sim_noise, axis=1)
        
        return [{
            "post": text,
            "relevance_score": round(float(score), 2),
            "matched_category": self.relevant_topics[best_rel_indices[i]] if ThresholdManager.get_decision(float(score)) != "Ignore" else "None",
            "confidence": f"{int(float(score) * 100)}%",
            "decision": ThresholdManager.get_decision(float(score))
        } for i, (text, score) in enumerate(zip(texts, np.clip(max_rel_scores - (max_noise_scores * 0.5), 0.0, 1.0)))]

    def semantic_search(self, query: str, corpus_texts: List[str], top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Advanced Semantic Search retrieving top_k most relevant texts from a given corpus.
        """
        if not query or not corpus_texts:
            return []
            
        query_emb = self.embedding_engine.encode([query])
        corpus_embs = self.embedding_engine.encode(corpus_texts)
        
        search_results = self.similarity_engine.semantic_search(query_emb, corpus_embs, top_k=top_k)
        
        results = []
        for hit in search_results[0]:  # Only retrieving for a single query
            results.append({
                "text": corpus_texts[hit['corpus_id']],
                "score": round(float(hit['score']), 4)
            })
        return results
