from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import util
import torch

class SimilarityEngine:
    @staticmethod
    def calculate_similarity(source_embeddings, target_embeddings):
        return cosine_similarity(source_embeddings, target_embeddings)

    @staticmethod
    def semantic_search(query_embeddings, corpus_embeddings, top_k: int = 5):
        """
        Advanced Semantic Search using PyTorch optimized tensor operations.
        """
        if not isinstance(query_embeddings, torch.Tensor):
            query_embeddings = torch.tensor(query_embeddings)
        if not isinstance(corpus_embeddings, torch.Tensor):
            corpus_embeddings = torch.tensor(corpus_embeddings)
            
        # util.semantic_search is highly optimized for vector retrieval
        hits = util.semantic_search(query_embeddings, corpus_embeddings, top_k=top_k)
        return hits
