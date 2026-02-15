from typing import List, Dict, Any
from pymongo.database import Database
from pymongo.collection import Collection


class CulturalSiteModel:
    def __init__(self, database: Database):
        self.database: Database = database
        self.collection: Collection = database["cultural_sites"]

    def get_all_sites(self) -> List[Dict[str, Any]]:
        try:
            # Query all documents, exclude _id field
            sites = list(self.collection.find({}, {"_id": 0}))
            return sites

        except Exception as e:
            raise Exception(f"Failed to retrieve cultural sites: {str(e)}")

    def get_site_by_id(self, site_id: str) -> Dict[str, Any]:
        try:
            site = self.collection.find_one({"id": site_id}, {"_id": 0})
            if site is None:
                raise Exception(f"Site with ID '{site_id}' not found")
            return site

        except Exception as e:
            raise Exception(f"Failed to retrieve site: {str(e)}")

    def get_sites_by_region(self, region: str) -> List[Dict[str, Any]]:
        try:
            sites = list(self.collection.find(
                {"region": {"$regex": region, "$options": "i"}},
                {"_id": 0}
            ))
            return sites

        except Exception as e:
            raise Exception(f"Failed to retrieve sites by region: {str(e)}")


def get_all_sites(database: Database) -> List[Dict[str, Any]]:
    model = CulturalSiteModel(database)
    return model.get_all_sites()
