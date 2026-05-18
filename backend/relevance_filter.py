import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import logging
from typing import List, Dict

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SemanticRelevanceFilter:
    """
    AI-powered Semantic Relevance Filtering System.
    Uses Sentence Transformers to filter out noise from business-relevant social media mentions.
    """
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        logging.info(f"Loading SentenceTransformer model: {model_name}")
        # all-MiniLM-L6-v2 is an excellent balance of speed and semantic accuracy
        self.model = SentenceTransformer(model_name)
        
        # Define high-signal business categories
        self.relevant_topics = [
            "customer complaint",
            "product feedback",
            "delivery issue",
            "refund problem",
            "pricing concern",
            "customer support issue",
            "product quality review",
            "feature request",
            "service experience",
            "purchase satisfaction"
        ]
        
        # Define noise categories to act as negative anchors
        self.noise_topics = [
            "funny meme and viral joke",
            "random unrelated chat and off-topic",
            "spam link, crypto and phishing",
            "engagement bait, like and retweet",
            "political debate and unrelated news"
        ]
        
        logging.info("Pre-computing embeddings for reference topics...")
        self.relevant_embeddings = self.model.encode(self.relevant_topics)
        self.noise_embeddings = self.model.encode(self.noise_topics)

    def evaluate_relevance(self, text: str) -> Dict[str, any]:
        if not text or not isinstance(text, str):
            return {"score": 0.0, "classification": "Ignore", "primary_matched_topic": "None"}

        # We can reuse the batch processing logic for a single text to keep it DRY
        result = self.process_batch([text])[0]
        return result

    def process_batch(self, texts: List[str]) -> List[Dict[str, any]]:
        """Processes a batch of texts using vectorized matrix multiplications for efficiency."""
        if not texts:
            return []
            
        # 1. Convert posts to semantic embeddings
        text_embs = self.model.encode(texts)
        
        # 2. Compare against both relevant signals and noise profiles
        sim_relevant = cosine_similarity(text_embs, self.relevant_embeddings)
        sim_noise = cosine_similarity(text_embs, self.noise_embeddings)
        
        max_rel_scores = np.max(sim_relevant, axis=1)
        best_rel_indices = np.argmax(sim_relevant, axis=1)
        max_noise_scores = np.max(sim_noise, axis=1)
        
        # 3. Penalize similarity to noise (Negative Anchoring)
        net_scores = np.clip(max_rel_scores - (max_noise_scores * 0.5), 0.0, 1.0)
        
        results = []
        for i in range(len(texts)):
            score = float(net_scores[i])
            
            # 4. Threshold Classification
            if score >= 0.55:
                cls = "Highly Relevant"
            elif score >= 0.40:
                cls = "Moderately Relevant"
            elif score >= 0.25:
                cls = "Low Relevance"
            else:
                cls = "Ignore"
                
            results.append({
                "score": score,
                "classification": cls,
                "primary_matched_topic": self.relevant_topics[best_rel_indices[i]] if cls != "Ignore" else "None"
            })
            
        return results