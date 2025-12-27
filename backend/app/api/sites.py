from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from pydantic import BaseModel
from app.models.site import CulturalSite
from app.services.database import get_database

class FavoriteRequest(BaseModel):
    site_name: str

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

@router.get("/sites/{site_name}", response_model=Dict[str, Any])
async def get_site_by_name(site_name: str):
    """
    Get a specific cultural site by name from MongoDB
    Excludes _id field from response
    Returns 404 if site not found
    """
    try:
        db = get_database()
        sites_collection = db["cultural_sites"]

        # Find site by name (case-insensitive search)
        site = sites_collection.find_one(
            {"name": {"$regex": f"^{site_name}$", "$options": "i"}},
            {"_id": 0}
        )

        if site is None:
            raise HTTPException(status_code=404, detail="Site not found")

        return site

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch site: {str(e)}")

@router.post("/favorites", response_model=Dict[str, str])
async def add_to_favorites(request: FavoriteRequest):
    """
    Add a cultural site to favorites collection
    Handles duplicate entries gracefully
    Returns confirmation message
    """
    try:
        db = get_database()
        favorites_collection = db["favorites"]

        # Check if site exists in cultural_sites collection first
        sites_collection = db["cultural_sites"]
        site_exists = sites_collection.find_one(
            {"name": {"$regex": f"^{request.site_name}$", "$options": "i"}}
        )

        if site_exists is None:
            raise HTTPException(status_code=404, detail="Site not found in cultural sites")

        # Check if already in favorites
        existing_favorite = favorites_collection.find_one(
            {"site_name": {"$regex": f"^{request.site_name}$", "$options": "i"}}
        )

        if existing_favorite:
            return {"message": f"'{request.site_name}' is already in your favorites"}

        # Add to favorites
        favorite_doc = {
            "site_name": request.site_name,
            "added_at": {"$date": {"$numberLong": str(int(__import__('time').time() * 1000))}}
        }

        result = favorites_collection.insert_one(favorite_doc)

        if result.inserted_id:
            return {"message": f"'{request.site_name}' has been added to your favorites"}
        else:
            raise HTTPException(status_code=500, detail="Failed to add to favorites")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add to favorites: {str(e)}")
