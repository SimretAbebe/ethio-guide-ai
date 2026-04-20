#!/usr/bin/env python3
"""
Sample Data Insertion Script for EthioGuide

This script inserts sample Ethiopian cultural sites into MongoDB Atlas.
"""

import os
from pymongo import MongoClient
from pymongo.database import Database
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_database() -> Database:
    """Connect to MongoDB and return database instance"""
    mongodb_uri = os.getenv("MONGODB_URI")
    database_name = os.getenv("DATABASE_NAME")

    if not mongodb_uri:
        raise ValueError("MONGODB_URI environment variable is not set")

    if not database_name:
        raise ValueError("DATABASE_NAME environment variable is not set")

    try:
        client = MongoClient(mongodb_uri)
        database = client[database_name]
        # Test the connection
        client.admin.command('ping')
        print("Successfully connected to MongoDB Atlas")
        return database

    except Exception as e:
        raise ConnectionError(f"Failed to connect to MongoDB: {str(e)}")

def insert_sample_sites(database: Database):
    """Insert sample Ethiopian cultural sites into the database"""

    # Sample Ethiopian cultural sites data
    sample_sites = [
        {
            "name": "Axum Obelisks",
            "description": "Ancient monolithic obelisks in Axum, UNESCO World Heritage Site, dating back to the 4th century AD. These towering granite monuments are among the most important archaeological sites in Ethiopia.",
            "location": "Axum, Tigray Region",
            "region": "Tigray",
            "category": "Historical Monument",
            "historical_significance": "Site of ancient Axumite civilization, one of Africa's oldest kingdoms",
            "visiting_hours": "8:00 AM - 5:00 PM",
            "entry_fee": 50.0,
            "images": [
                "https://images.unsplash.com/photo-1627311754972-20760472fac8?auto=format&fit=crop&w=1200&q=80",
                "https://images.unsplash.com/photo-1596394516093-501ba68a0ba6?auto=format&fit=crop&w=1200&q=80"
            ],
            "coordinates": {"latitude": 14.1271, "longitude": 38.7223}
        },
        {
            "name": "Rock-Hewn Churches of Lalibela",
            "description": "Eleven medieval monolithic cave churches carved out of solid volcanic tuff in Lalibela. UNESCO World Heritage Site representing the 'New Jerusalem'.",
            "location": "Lalibela, Amhara Region",
            "region": "Amhara",
            "category": "Religious Site",
            "historical_significance": "Built in the 12th-13th centuries during the Zagwe dynasty, representing outstanding medieval Ethiopian architecture",
            "visiting_hours": "6:00 AM - 6:00 PM",
            "entry_fee": 75.0,
            "images": [
                "https://images.unsplash.com/photo-1549468057-5b7fb2700d22?auto=format&fit=crop&w=1200&q=80",
                "https://images.unsplash.com/photo-1621252179027-94459d278660?auto=format&fit=crop&w=1200&q=80"
            ],
            "coordinates": {"latitude": 12.0309, "longitude": 39.0476}
        },
        {
            "name": "Simien Mountains National Park",
            "description": "UNESCO World Heritage Site featuring dramatic mountain landscapes, endemic wildlife, and the deepest gorge in Africa. Home to the endangered Gelada baboon and Ethiopian wolf.",
            "location": "Simien Mountains, Amhara Region",
            "region": "Amhara",
            "category": "Natural Site",
            "historical_significance": "Sacred mountains in Ethiopian Orthodox tradition, ancient human habitation sites",
            "visiting_hours": "6:00 AM - 6:00 PM",
            "entry_fee": 30.0,
            "images": [
                "https://images.unsplash.com/photo-1533221919575-f7166133beff?auto=format&fit=crop&w=1200&q=80",
                "https://images.unsplash.com/photo-1523821741446-edb2b68bb7a0?auto=format&fit=crop&w=1200&q=80"
            ],
            "coordinates": {"latitude": 13.1833, "longitude": 38.0667}
        },
        {
            "name": "Fasil Ghebbi (Gondar Castle)",
            "description": "17th-century royal enclosure and castle complex in Gondar, former capital of Ethiopia. UNESCO World Heritage Site showcasing Baroque and local architectural styles.",
            "location": "Gondar, Amhara Region",
            "region": "Amhara",
            "category": "Historical Monument",
            "historical_significance": "Capital of Ethiopia during the 17th-19th centuries, center of the Solomonic dynasty",
            "visiting_hours": "8:00 AM - 5:00 PM",
            "entry_fee": 25.0,
            "images": [
                "https://images.unsplash.com/photo-1565538403986-ec938186178a?auto=format&fit=crop&w=1200&q=80",
                "https://images.unsplash.com/photo-1518131359149-83c921509176?auto=format&fit=crop&w=1200&q=80"
            ],
            "coordinates": {"latitude": 12.6072, "longitude": 37.4664}
        },
        {
            "name": "Lower Valley of the Awash",
            "description": "UNESCO World Heritage Site containing important paleoanthropological sites. Location of the discovery of early hominids including 'Lucy' (Australopithecus afarensis).",
            "location": "Awash Valley, Afar Region",
            "region": "Afar",
            "category": "Archaeological Site",
            "historical_significance": "Key site for understanding human evolution, contains fossils dating back 4 million years",
            "visiting_hours": "8:00 AM - 5:00 PM",
            "entry_fee": 20.0,
            "images": [
                "https://images.unsplash.com/photo-1523438097201-512ae7d59c44?auto=format&fit=crop&w=1200&q=80"
            ],
            "coordinates": {"latitude": 11.1333, "longitude": 40.5833}
        }
    ]

    try:
        collection = database["cultural_sites"]

        # Insert the sample sites
        result = collection.insert_many(sample_sites)

        print(f"Successfully inserted {len(result.inserted_ids)} sample cultural sites into MongoDB")
        print("Sites inserted:")
        for i, site in enumerate(sample_sites, 1):
            print(f"   {i}. {site['name']} - {site['location']}")

    except Exception as e:
        print(f"Error inserting sample data: {str(e)}")
        raise

def main():
    """Main function to run the data insertion script"""
    try:
        print("Starting EthioGuide sample data insertion...")

        # Get database connection
        database = get_database()

        # Insert sample sites
        insert_sample_sites(database)

        print("\nSample data insertion completed successfully!")
        print("Your MongoDB database now contains Ethiopian cultural sites data.")

    except Exception as e:
        print(f"\n Script failed: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()
