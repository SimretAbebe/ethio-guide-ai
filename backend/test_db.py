from app.services.database import get_database

try:
    db = get_database()
    print("Connected to MongoDB!")
    
    sites = list(db.cultural_sites.find({}, {"_id": 0, "name": 1}))
    print(f"Found {len(sites)} sites:")
    for site in sites:
        print(f"  - {site.get('name')}")
except Exception as e:
    print(f"Error: {e}")
