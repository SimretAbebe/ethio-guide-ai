from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from pydantic import BaseModel
from app.models.site import CulturalSite
from app.services.database import get_database

class FavoriteRequest(BaseModel):
    site_name: str

class ReviewRequest(BaseModel):
    user_name: str
    rating: int
    comment: str

router = APIRouter()

@router.get("/sites", response_model=List[CulturalSite])
async def get_all_sites(
    search: str = None,
    category: str = None,
    region: str = None,
    sort_by: str = "name",
    order: str = "asc"
):
    try:
        db = get_database()
        sites_collection = db["cultural_sites"]

        # Build query filter
        query_filter = {}
        
        if search:
            # Search in multiple fields
            query_filter["$or"] = [
                {"name": {"$regex": search, "$options": "i"}},
                {"description": {"$regex": search, "$options": "i"}},
                {"location": {"$regex": search, "$options": "i"}}
            ]
        
        if category:
            query_filter["category"] = {"$regex": f"^{category}$", "$options": "i"}
        
        if region:
            query_filter["region"] = {"$regex": f"^{region}$", "$options": "i"}

        # Define sort mapping
        sort_mapping = {
            "name": "name",
            "date": "created_at",
            "popularity": "average_rating"
        }
        
        sort_field = sort_mapping.get(sort_by, "name")
        sort_order = 1 if order == "asc" else -1

        # Get sites with filter, exclude _id, and apply sort
        sites = list(sites_collection.find(query_filter, {"_id": 0}).sort(sort_field, sort_order))

        return sites

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch sites: {str(e)}")

@router.get("/sites/{site_name}", response_model=CulturalSite)
async def get_site_by_name(site_name: str):
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

@router.get("/favorites", response_model=List[Dict[str, Any]])
async def get_all_favorites():

    try:
        db = get_database()
        favorites_collection = db["favorites"]
        sites_collection = db["cultural_sites"]

        # Get all favorites
        favorites = list(favorites_collection.find({}, {"_id": 0}))

        # Enrich with full site details
        enriched_favorites = []
        for fav in favorites:
            site = sites_collection.find_one(
                {"name": {"$regex": f"^{fav['site_name']}$", "$options": "i"}},
                {"_id": 0}
            )
            if site:
                enriched_favorites.append(site)

        return enriched_favorites

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch favorites: {str(e)}")

@router.post("/favorites", response_model=Dict[str, str])
async def add_to_favorites(request: FavoriteRequest):
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

@router.delete("/favorites/{site_name}", response_model=Dict[str, str])
async def remove_from_favorites(site_name: str):
    try:
        db = get_database()
        favorites_collection = db["favorites"]

        # Find and delete the favorite
        result = favorites_collection.delete_one(
            {"site_name": {"$regex": f"^{site_name}$", "$options": "i"}}
        )

        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Site not found in favorites")

        return {"message": f"'{site_name}' has been removed from your favorites"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to remove from favorites: {str(e)}")
@router.post("/sites/{site_name}/reviews", response_model=Dict[str, Any])
async def add_review(site_name: str, request: ReviewRequest):
    try:
        db = get_database()
        sites_collection = db["cultural_sites"]

        # Find site
        site = sites_collection.find_one(
            {"name": {"$regex": f"^{site_name}$", "$options": "i"}}
        )

        if site is None:
            raise HTTPException(status_code=404, detail="Site not found")

        # Create review object
        import datetime
        review = {
            "user_name": request.user_name,
            "rating": request.rating,
            "comment": request.comment,
            "created_at": datetime.datetime.now().isoformat()
        }

        # Get existing reviews or initialize
        reviews = site.get("reviews", [])
        reviews.append(review)

        # Calculate new average rating
        total_rating = sum(r["rating"] for r in reviews)
        average_rating = total_rating / len(reviews)

        # Update site in DB
        result = sites_collection.update_one(
            {"name": {"$regex": f"^{site_name}$", "$options": "i"}},
            {"$set": {
                "reviews": reviews,
                "average_rating": average_rating
            }}
        )

        if result.modified_count > 0:
            return {
                "message": "Review added successfully",
                "average_rating": average_rating,
                "review": review
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to update site with review")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add review: {str(e)}")

@router.get("/recommendations", response_model=List[Dict[str, Any]])
async def get_recommendations(top_k: int = 5):
    """
    Get personalized site recommendations based on user's favorites.
    Uses cached AI embeddings for high performance.
    """
    try:
        from app.services.ai_service import get_ai_service
        ai_service = get_ai_service()
        
        db = get_database()
        favorites_collection = db["favorites"]
        sites_collection = db["cultural_sites"]

        # Ensure cache is populated (or at least attempt to)
        all_sites = list(sites_collection.find({}, {"_id": 0}))
        if not ai_service.site_embeddings_cache:
            ai_service.update_site_embeddings_cache(all_sites)
        
        favorites = list(favorites_collection.find({}, {"_id": 0}))
        if not favorites:
            # Fallback to top rated sites
            top_sites = list(sites_collection.find({}, {"_id": 0}).sort("average_rating", -1).limit(top_k))
            return top_sites

        favorite_site_names = [f["site_name"] for f in favorites]
        
        # Get embeddings from cache
        favorite_embeddings = ai_service.get_cached_embeddings(favorite_site_names)
        
        # If any favorites are missing from cache (newly added?), update cache
        if favorite_embeddings.shape[0] < len(favorite_site_names):
            ai_service.update_site_embeddings_cache(all_sites)
            favorite_embeddings = ai_service.get_cached_embeddings(favorite_site_names)

        if favorite_embeddings.size == 0:
            return []

        # Get all embeddings from cache
        all_site_names = [s["name"] for s in all_sites]
        all_embeddings = ai_service.get_cached_embeddings(all_site_names)

        # Get recommendations
        recommendations = ai_service.get_recommendations(
            favorite_embeddings, 
            all_embeddings, 
            all_sites, 
            top_k=top_k + len(favorite_site_names) 
        )

        # Filter out already favorited sites
        filtered_recommendations = [
            r for r in recommendations 
            if r["name"] not in favorite_site_names
        ][:top_k]

        return filtered_recommendations

    except Exception as e:
        print(f"Error in recommendations: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get recommendations: {str(e)}")
