import os
import datetime
from pymongo import MongoClient
from dotenv import load_dotenv


load_dotenv()

def get_database():
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
        },
        "Fasil Ghebbi (Gondar Castle)": {
            "images": [
                "https://as1.ftcdn.net/v2/jpg/02/04/12/64/1000_F_204126439_DuDTOYeoLxAQZPppUkUoTjEiGEiDqSst.jpg",
                "https://as2.ftcdn.net/v2/jpg/02/68/76/31/1000_F_268763137_DuDTOYeoLxAQZPppUkUoTjEiGEiDqSst.jpg"
            ],
            "reviews": [
                {"user_name": "Mulugeta T.", "rating": 5, "comment": "The Camelot of Africa! Incredible architecture.", "created_at": datetime.datetime.now().isoformat()}
            ],
            "average_rating": 5.0
        },
        "Lower Valley of the Awash": {
            "images": [
                "https://as2.ftcdn.net/v2/jpg/06/02/05/15/1000_F_602051533_nw1p3jZ9k9Q9fM65ut6ZYcL2U5o4Pgik.jpg"
            ],
            "reviews": [
                {"user_name": "Dr. Smith", "rating": 4, "comment": "A humbling experience to see where Lucy was found.", "created_at": datetime.datetime.now().isoformat()}
            ],
            "average_rating": 4.0
        },
        "Harar Jugol": {
            "description": "The fortified historic town of Harar Jugol is located in the eastern part of the country on a plateau. It is considered the 'fourth holy city of Islam' and features 82 mosques and 102 shrines.",
            "location": "Harar, Harari Region",
            "region": "Harari",
            "category": "Historical Town",
            "historical_significance": "A major commercial center and a sacred city in Islamic culture since the 16th century.",
            "visiting_hours": "6:00 AM - 10:00 PM",
            "entry_fee": 100.0,
            "coordinates": {"latitude": 9.3131, "longitude": 42.1227},
            "images": [
                "https://qiraatafrican.com/en/wp-content/uploads/2025/08/harar-main-gate-ethiopia-750x375.jpg"
            ],
            "reviews": [
                {"user_name": "Fatuma Y.", "rating": 5, "comment": "The hyena feeding ceremony is unforgettable!", "created_at": datetime.datetime.now().isoformat()}
            ],
            "average_rating": 5.0
        },
        "Konso Cultural Landscape": {
            "description": "A 55 sq km arid property of stone-walled terraces and fortified settlements in the Konso highlands. This landscape is a spectacular example of a living cultural tradition stretching back 21 generations.",
            "location": "Konso, SNNPR",
            "region": "SNNPR",
            "category": "Cultural Landscape",
            "historical_significance": "Famous for its wooden statues (wagas), erected in memory of grandfathers and warriors.",
            "visiting_hours": "8:00 AM - 6:00 PM",
            "entry_fee": 80.0,
            "coordinates": {"latitude": 5.3412, "longitude": 37.4404},
            "images": [
                "https://media-cdn.tripadvisor.com/media/photo-s/1c/70/de/2b/konso-cultural-landscape.jpg"
            ],
            "reviews": [
                {"user_name": "Kassa G.", "rating": 4, "comment": "The terraces are a masterpiece of traditional engineering.", "created_at": datetime.datetime.now().isoformat()}
            ],
            "average_rating": 4.0
        }
    }
    
    collection = database["cultural_sites"]
    updated_count = 0
    
    for site_name, updates in site_updates.items():
        result = collection.update_one(
            {"name": site_name},
            {"$set": updates},
            upsert=True
        )
        if result.modified_count > 0 or result.upserted_id:
            updated_count += 1
            print(f"+ Processed '{site_name}' (Updated/Inserted)")
    
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
