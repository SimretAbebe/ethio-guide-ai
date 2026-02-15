import httpx
import json

def test_sorting():
    base_url = "http://127.0.0.1:8001"
    
    print("Testing sorting by name (asc)...")
    response = httpx.get(f"{base_url}/sites?sort_by=name&order=asc", timeout=30.0)
    sites = response.json()
    names = [s["name"] for s in sites]
    print(f"Names: {names}")
    assert names == sorted(names)
    
    print("\nTesting sorting by popularity (desc)...")
    response = httpx.get(f"{base_url}/sites?sort_by=popularity&order=desc", timeout=30.0)
    sites = response.json()
    ratings = [s["average_rating"] for s in sites]
    print(f"Ratings: {ratings}")
    assert ratings == sorted(ratings, reverse=True)
    
    print("\nTesting sorting by date (desc)...")
    response = httpx.get(f"{base_url}/sites?sort_by=date&order=desc", timeout=30.0)
    sites = response.json()
    dates = [s["created_at"] for s in sites]
    print(f"Dates: {dates}")
    assert dates == sorted(dates, reverse=True)
    
    print("\nAll backend sorting tests passed!")

if __name__ == "__main__":
    try:
        test_sorting()
    except Exception as e:
        print(f"Test failed: {e}")
