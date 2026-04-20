from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.sites import router as sites_router
from app.api.ai import router as ai_router

import os

app = FastAPI(
    title="EthioGuide API",
    description="API for Ethiopian cultural sites and heritage information",
    version="1.0.0"
)

# CORS configuration
allowed_origins_str = os.getenv("ALLOWED_ORIGINS", "*")
allowed_origins = [origin.strip() for origin in allowed_origins_str.split(",") if origin.strip()]

# If "*" is in the list, or if we're not in production, allow all origins for easier debugging
if "*" in allowed_origins or os.getenv("ENVIRONMENT", "development") != "production":
    allowed_origins = ["*"]

print(f"CORS: Allowing origins: {allowed_origins}")

@app.on_event("startup")
async def startup_event():
    print("EthioGuide API is starting up...")
    print(f"Environment: {os.getenv('ENVIRONMENT', 'development')}")
    # We don't connect to DB here to keep startup fast, 
    # but we can verify the environment variables exist
    if not os.getenv("MONGODB_URI"):
        print("CRITICAL: MONGODB_URI is not set!")
    if not os.getenv("GOOGLE_API_KEY"):
        print("WARNING: GOOGLE_API_KEY is not set. AI Chat will be in fallback mode.")

@app.on_event("shutdown")
async def shutdown_event():
    print("EthioGuide API is shutting down...")
    from app.services.database import db_connection
    db_connection.close()

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(sites_router)
app.include_router(ai_router)

@app.get("/")
async def root():
    """Root endpoint - Welcome message"""
    return {"message": "Welcome to EthioGuide API"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
