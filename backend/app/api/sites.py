from fastapi import APIRouter, HTTPException
from typing import List
from app.models.site import CulturalSite
from app.services.database import get_database

router = APIRouter()

@router.get("/sites", response_model=List[CulturalSite])
async def get_all_sites():
    """
    Get all cultural sites from MongoDB
    Excludes _id field from response
    """
    try:
        db = get_database()
        sites_collection = db["cultural_sites"]

        # Get all sites, exclude _id
        sites = list(sites_collection.find({}, {"_id": 0}))

        return sites

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch sites: {str(e)}")
