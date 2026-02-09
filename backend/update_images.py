#!/usr/bin/env python3
"""
Update existing cultural sites with real image URLs
"""

import os
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

def update_site_images(database):
    """Update sites with real image URLs"""
    
    # Map site names to their image URLs (from Home.tsx)
    image_mappings = {
        "Rock-Hewn Churches of Lalibela": [
            "https://as2.ftcdn.net/v2/jpg/04/16/05/59/1000_F_416055968_sBw34oi95UakEtB9UIbj1tOoiV4qr4Ja.jpg"
        ],
        "Simien Mountains National Park": [
            "https://as2.ftcdn.net/v2/jpg/01/07/88/63/1000_F_107886352_xGZ7Ru6wyeccVj8arEGwIMGXnoMHcHAQ.jpg"
        ],
        "Axum Obelisks": [
            "https://as2.ftcdn.net/v2/jpg/05/54/73/31/1000_F_554733188_uHZ4HvipmNllQfZ5uMyRS7MDXRSVxDrQ.jpg"
        ],
        "Fasil Ghebbi (Gondar Castle)": [
            "https://as1.ftcdn.net/v2/jpg/02/04/12/64/1000_F_204126439_DuDTOYeoLxAQZPppUkUoTjEiGEiDqSst.jpg"
        ],
        "Lower Valley of the Awash": [
            "https://as2.ftcdn.net/v2/jpg/06/02/05/15/1000_F_602051533_nw1p3jZ9k9Q9fM65ut6ZYcL2U5o4Pgik.jpg"
        ]
    }
    
    collection = database["cultural_sites"]
    updated_count = 0
    
    for site_name, images in image_mappings.items():
        result = collection.update_one(
            {"name": site_name},
            {"$set": {"images": images}}
        )
        if result.modified_count > 0:
            updated_count += 1
            print(f"✓ Updated '{site_name}' with image URL")
        else:
            print(f"✗ Site '{site_name}' not found or already has images")
    
    print(f"\n Successfully updated {updated_count} sites with images")

def main():
    """Main function"""
    try:
        print("Updating cultural sites with image URLs...\n")
        database = get_database()
        update_site_images(database)
        print("\nUpdate completed!")
    except Exception as e:
        print(f"\n❌ Failed: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()
