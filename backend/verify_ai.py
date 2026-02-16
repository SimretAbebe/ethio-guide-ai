from app.services.ai_service import AIService
import numpy as np

def test_ai_service():
    print("Initializing AIService...")
    ai = AIService()
    
    texts = ["Lalibela Rock-Hewn Churches", "The obelisks of Axum"]
    print(f"Generating embeddings for: {texts}")
    embeddings = ai.generate_embeddings(texts)
    
    print(f"Generated embeddings shape: {embeddings.shape}")
    
    
    sim = ai.get_recommendations(
        user_favorite_embeddings=embeddings[0:1], # Lalibela
        all_site_embeddings=embeddings,
        all_sites=[{"name": "Lalibela", "description": texts[0]}, {"name": "Axum", "description": texts[1]}],
        top_k=2
    )
    
    print("Recommendations test result:")
    for r in sim:
        print(f"- {r['name']} (score: {r['score']:.4f})")

if __name__ == "__main__":
    try:
        test_ai_service()
        print("\nAI Service is working correctly!")
    except Exception as e:
        print(f"Error testing AI service: {e}")
