import torch
from sentence_transformers import SentenceTransformer
import logging

class EmbeddingEngine:
    def __init__(self, model_name: str = 'BAAI/bge-large-en-v1.5'):
        # Hardware acceleration detection for advanced deployment
        self.device = 'cuda' if torch.cuda.is_available() else 'mps' if torch.backends.mps.is_available() else 'cpu'
        logging.info(f"Loading SentenceTransformer model: {model_name} on {self.device}")
        
        # BAAI/bge-large-en-v1.5 is a state-of-the-art text embedding model
        self.model = SentenceTransformer(model_name, device=self.device)

    def encode(self, texts, normalize_embeddings: bool = True):
        # Normalizing embeddings enables much faster dot-product similarity search
        return self.model.encode(texts, normalize_embeddings=normalize_embeddings)
