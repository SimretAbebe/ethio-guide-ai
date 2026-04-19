from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.database import get_database

router = APIRouter(prefix="/ai", tags=["AI"])

class ChatRequest(BaseModel):
    message: str
    context: str = ""

@router.post("/chat")
async def chat_with_guide(request: ChatRequest):
    try:
        from app.services.ai_service import get_ai_service
        ai_service = get_ai_service()
        
        # Build context from database if not explicitly provided
        context = request.context
        if not context:
            db = get_database()
            sites_collection = db["cultural_sites"]
            # Get key info from sites for context
            sites = list(sites_collection.find({}, {"name": 1, "description": 1, "region": 1, "_id": 0}).limit(15))
            
            site_info = []
            for s in sites:
                # Keep descriptions short to save tokens
                desc = s.get('description', '')[:100].strip()
                if desc:
                    desc += "..."
                info = f"- {s['name']} ({s.get('region', 'Ethiopia')}): {desc}"
                site_info.append(info)
            
            context = "You are an expert Ethiopian tour guide AI. Be informative, enthusiastic, and culturally respectful.\n"
            context += "Information about some key sites in Ethiopia:\n"
            context += "\n".join(site_info)
            context += "\n\nAnswer the visitor's question using this context and your extensive knowledge of Ethiopian heritage."

        response = ai_service.get_chat_response(request.message, context)
        return {"response": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Chat failed: {str(e)}")
