from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.ai_service import get_ai_service
from app.services.database import get_database

router = APIRouter(prefix="/ai", tags=["AI"])

class ChatRequest(BaseModel):
    message: str
    context: str = ""

@router.post("/chat")
async def chat_with_guide(request: ChatRequest):
    try:
        ai_service = get_ai_service()
        
        # If context is empty, try to provide some default context about Ethiopia
        context = request.context
        if not context:
            db = get_database()
            sites_collection = db["cultural_sites"]
            # Get names of some top sites for context
            sites = list(sites_collection.find({}, {"name": 1, "_id": 0}).limit(5))
            site_names = [s["name"] for s in sites]
            context = f"You are a helpful Ethiopian tour guide. Here are some sites I know about: {', '.join(site_names)}."

        response = ai_service.get_chat_response(request.message, context)
        return {"response": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Chat failed: {str(e)}")
