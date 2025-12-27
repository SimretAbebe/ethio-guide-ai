"""
Cultural Sites MongoDB Operations Module

This module provides database operations for cultural sites data.
Handles all MongoDB interactions for the cultural_sites collection.
"""

from typing import List, Dict, Any
from pymongo.database import Database
from pymongo.collection import Collection


class CulturalSiteModel:
    """
    Model class for handling cultural sites MongoDB operations.
    """

    def __init__(self, database: Database):
        """
        Initialize the model with a MongoDB database instance.

        Args:
            database: MongoDB database instance
        """
        self.database: Database = database
        self.collection: Collection = database["cultural_sites"]

    def get_all_sites(self) -> List[Dict[str, Any]]:
        """
        Retrieve all cultural sites from the database.

        Returns:
            List of dictionaries containing cultural site data (excluding _id field)

        Raises:
            Exception: If database operation fails
        """
        try:
            # Query all documents, exclude _id field
            sites = list(self.collection.find({}, {"_id": 0}))
            return sites

        except Exception as e:
            raise Exception(f"Failed to retrieve cultural sites: {str(e)}")

    def get_site_by_id(self, site_id: str) -> Dict[str, Any]:
        """
        Retrieve a specific cultural site by ID.

        Args:
            site_id: The ID of the site to retrieve

        Returns:
            Dictionary containing site data (excluding _id field)

        Raises:
            Exception: If database operation fails or site not found
        """
        try:
            site = self.collection.find_one({"id": site_id}, {"_id": 0})
            if site is None:
                raise Exception(f"Site with ID '{site_id}' not found")
            return site

        except Exception as e:
            raise Exception(f"Failed to retrieve site: {str(e)}")

    def get_sites_by_region(self, region: str) -> List[Dict[str, Any]]:
        """
        Retrieve cultural sites filtered by region.

        Args:
            region: The region to filter by

        Returns:
            List of dictionaries containing cultural site data for the specified region
        """
        try:
            sites = list(self.collection.find(
                {"region": {"$regex": region, "$options": "i"}},
                {"_id": 0}
            ))
            return sites

        except Exception as e:
            raise Exception(f"Failed to retrieve sites by region: {str(e)}")


def get_all_sites(database: Database) -> List[Dict[str, Any]]:
    """
    Convenience function to get all cultural sites.

    Args:
        database: MongoDB database instance

    Returns:
        List of dictionaries containing all cultural site data
    """
    model = CulturalSiteModel(database)
    return model.get_all_sites()
