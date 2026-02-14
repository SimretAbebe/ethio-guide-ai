from pydantic import BaseModel
from typing import Optional, List
from bson import ObjectId

class Review(BaseModel):
    """Review model for cultural sites"""
    user_name: str
    rating: int  # 1-5
    comment: str
    created_at: Optional[str] = None

class CulturalSite(BaseModel):
    """Cultural site model"""
    name: str
    description: str
    location: str
    region: str
    category: str
    historical_significance: Optional[str] = None
    visiting_hours: Optional[str] = None
    entry_fee: Optional[float] = None
    images: Optional[List[str]] = []
    coordinates: Optional[dict] = None
    reviews: Optional[List[Review]] = []
    average_rating: Optional[float] = 0.0

    class Config:
        # Allow ObjectId conversion
        json_encoders = {
            ObjectId: str
        }
