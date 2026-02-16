from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Optional
import os

class AIService:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the AI Service with a sentence-transformer model.
        Default model 'all-MiniLM-L6-v2' is fast and efficient.
        """
        self.model = SentenceTransformer(model_name)

    def generate_embeddings(self, texts: List[str]) -> np.ndarray:
        """
        Generate embeddings for a list of texts.
        """
        if not texts:
            return np.array([])
        return self.model.encode(texts)

    def get_recommendations(
        self, 
        user_favorite_embeddings: np.ndarray, 
        all_site_embeddings: np.ndarray, 
        all_sites: List[Dict], 
        top_k: int = 5
    ) -> List[Dict]:
        if user_favorite_embeddings.size == 0 or all_site_embeddings.size == 0:
            return []
        user_profile = np.mean(user_favorite_embeddings, axis=0).reshape(1, -1)
        

        top_indices = np.argsort(similarities)[::-1]
        
     
        favorite_names = {site.get("name") for site in all_sites if any(np.array_equal(self.model.encode([site.get("description", "")]), emb) for emb in user_favorite_embeddings)}
       
        
        recommendations = []
        for idx in top_indices:
            site = all_sites[idx]
            recommendations.append({
                "name": site.get("name"),
                "score": float(similarities[idx]),
                "description": site.get("description"),
                "image": site.get("images")[0] if site.get("images") else None
            })
            if len(recommendations) >= top_k:
                break
            
        return recommendations
        
ai_service = None

def get_ai_service() -> AIService:
    global ai_service
    if ai_service is None:
        ai_service = AIService()
    return ai_service
