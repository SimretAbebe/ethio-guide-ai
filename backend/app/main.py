from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.sites import router as sites_router

# Create FastAPI app instance
app = FastAPI(
    title="EthioGuide API",
    description="API for Ethiopian cultural sites and heritage information",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(sites_router)

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
    uvicorn.run(app, host="0.0.0.0", port=8000)
