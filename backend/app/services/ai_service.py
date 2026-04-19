import google.generativeai as genai
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AIService:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the AI Service with a sentence-transformer model and Gemini.
        """
        # For recommendations
        self._model = None
        self._model_name = model_name
        self.site_embeddings_cache = {} # site_name -> embedding
        
        # For ChatBot
        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            self.chat_model = genai.GenerativeModel('gemini-pro')
        else:
            self.chat_model = None
    @property
    def model(self):
        if self._model is None:
            print(f"Loading SentenceTransformer model: {self._model_name}...")
            self._model = SentenceTransformer(self._model_name)
        return self._model

    def generate_embeddings(self, texts: List[str]) -> np.ndarray:
        if not texts:
            return np.array([])
        return self.model.encode(texts)

    def update_site_embeddings_cache(self, sites: List[Dict]):
        """
        Pre-calculate and cache embeddings for all sites.
        Each site must have a 'name' and 'description'.
        """
        if not sites:
            return
        
        descriptions = [s.get("description", "") for s in sites]
        names = [s.get("name") for s in sites]
        
        embeddings = self.generate_embeddings(descriptions)
        
        for name, embedding in zip(names, embeddings):
            self.site_embeddings_cache[name] = embedding
            
        print(f"Cached embeddings for {len(sites)} sites.")

    def get_cached_embeddings(self, names: List[str]) -> np.ndarray:
        """Retrieve embeddings from cache for specific sites."""
        embeddings = []
        for name in names:
            if name in self.site_embeddings_cache:
                embeddings.append(self.site_embeddings_cache[name])
        return np.array(embeddings) if embeddings else np.array([])

    def get_recommendations(
        self, 
        user_favorite_embeddings: np.ndarray, 
        all_site_embeddings: np.ndarray, 
        all_sites: List[Dict], 
        top_k: int = 5
    ) -> List[Dict]:
        if user_favorite_embeddings.size == 0 or all_site_embeddings.size == 0:
            return []
        
        # Simple averaging for user profile
        user_profile = np.mean(user_favorite_embeddings, axis=0).reshape(1, -1)
        
        similarities = cosine_similarity(user_profile, all_site_embeddings).flatten()
        top_indices = np.argsort(similarities)[::-1]
        
        recommendations = []
        for idx in top_indices:
            site = all_sites[idx]
            recommendations.append({
                "name": site.get("name"),
                "score": float(similarities[idx]),
                "description": site.get("description"),
                "location": site.get("region") or site.get("location"),
                "image": site.get("images")[0] if site.get("images") else None
            })
            if len(recommendations) >= top_k:
                break
            
        return recommendations
        
    def get_chat_response(self, prompt: str, context: str) -> str:
        if not self.chat_model:
            # Fallback to simple rule-based response
            if "lalibela" in prompt.lower():
                return "Lalibela is famous for its rock-hewn churches, built in the 12th and 13th centuries. It's often called the 'Eighth Wonder of the World'."
            elif "axum" in prompt.lower():
                return "Axum was the center of the Aksumite Empire. It's known for its ancient obelisks and the Church of St. Mary of Zion, which is said to house the Ark of the Covenant."
            else:
                return f"I'm your EthioGuide AI. Please set your GOOGLE_API_KEY in the backend .env file to enable full chat capabilities. For now, I can tell you basic info about sites like Lalibela or Axum. You asked: '{prompt}'"

        try:
            full_prompt = f"Context: {context}\n\nUser Question: {prompt}\n\nPlease provide a helpful and informative response as an experienced Ethiopian tour guide. Be engaging, accurate, and respectful."
            response = self.chat_model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            print(f"Error calling Gemini API: {str(e)}")
            return "I'm sorry, I'm having trouble processing your request right now. Please try again later."

_ai_service_instance = None

def get_ai_service() -> AIService:
    global _ai_service_instance
    if _ai_service_instance is None:
        _ai_service_instance = AIService()
    return _ai_service_instance
