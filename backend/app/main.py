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
allowed_origins_str = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173")
allowed_origins = [origin.strip() for origin in allowed_origins_str.split(",")]

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
