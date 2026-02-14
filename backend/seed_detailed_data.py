#!/usr/bin/env python3
"""
Seed cultural sites with multiple images and sample reviews
"""

import os
import datetime
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_database():
    """Connect to MongoDB and return database instance"""
    mongodb_uri = os.getenv("MONGODB_URI")
    database_name = os.getenv("DATABASE_NAME")

    if not mongodb_uri or not database_name:
        raise ValueError("Database environment variables are not set")

    try:
        client = MongoClient(mongodb_uri)
        database = client[database_name]
        client.admin.command('ping')
        print("Successfully connected to MongoDB Atlas")
        return database
    except Exception as e:
        raise ConnectionError(f"Failed to connect to MongoDB: {str(e)}")

def seed_detailed_data(database):
    """Seed detailed data for sites"""
    
    site_updates = {
        "Rock-Hewn Churches of Lalibela": {
            "images": [
                "https://as2.ftcdn.net/v2/jpg/04/16/05/59/1000_F_416055968_sBw34oi95UakEtB9UIbj1tOoiV4qr4Ja.jpg",
                "https://as2.ftcdn.net/v2/jpg/02/76/89/63/1000_F_276896347_uXWofO5XpL1hVjXlA3S6WjG7iQyIq8gJ.jpg",
                "https://as1.ftcdn.net/v2/jpg/00/61/88/24/1000_F_61882414_tO5XW5oM0uTzE6Uu5O6WjG7iQyIq8gJ.jpg"
            ],
            "reviews": [
                {"user_name": "Abebe B.", "rating": 5, "comment": "Breathtaking architecture. A must-see!", "created_at": datetime.datetime.now().isoformat()},
                {"user_name": "Sara M.", "rating": 4, "comment": "Very crowded but worth the visit.", "created_at": datetime.datetime.now().isoformat()}
            ],
            "average_rating": 4.5
        },
        "Simien Mountains National Park": {
            "images": [
                "https://as2.ftcdn.net/v2/jpg/01/07/88/63/1000_F_107886352_xGZ7Ru6wyeccVj8arEGwIMGXnoMHcHAQ.jpg",
                "https://as1.ftcdn.net/v2/jpg/00/76/89/63/1000_F_76896347_uXWofO5XpL1hVjXlA3S6WjG7iQyIq8gJ.jpg"
            ],
            "reviews": [
                {"user_name": "Dawit K.", "rating": 5, "comment": "Best hiking experience in Africa!", "created_at": datetime.datetime.now().isoformat()}
            ],
            "average_rating": 5.0
        },
        "Axum Obelisks": {
            "images": [
                "https://as2.ftcdn.net/v2/jpg/05/54/73/31/1000_F_554733188_uHZ4HvipmNllQfZ5uMyRS7MDXRSVxDrQ.jpg",
                "https://as2.ftcdn.net/v2/jpg/02/04/12/64/1000_F_204126439_DuDTOYeoLxAQZPppUkUoTjEiGEiDqSst.jpg"
            ],
            "reviews": [
                {"user_name": "Hassan A.", "rating": 4, "comment": "Rich history, very impressive monuments.", "created_at": datetime.datetime.now().isoformat()}
            ],
            "average_rating": 4.0
        }
    }
    
    collection = database["cultural_sites"]
    updated_count = 0
    
    for site_name, updates in site_updates.items():
        result = collection.update_one(
            {"name": site_name},
            {"$set": updates}
        )
        if result.modified_count > 0:
            updated_count += 1
            print(f"✓ Updated '{site_name}' with detailed data")
    
    print(f"\n Successfully updated {updated_count} sites")

def main():
    """Main function"""
    try:
        print("Seeding detailed data for sites...\n")
        database = get_database()
        seed_detailed_data(database)
        print("\nSeed completed!")
    except Exception as e:
        print(f"\n Failed: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()
