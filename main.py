"""
TikTok CDN Demo

⚠️  Demo Purpose Only ⚠️
This is a proof-of-concept demonstration showing how CDN image uploads
can be exploited for video hosting through HLS playlist manipulation.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from config import APP_NAME, APP_VERSION, HOST, PORT
from modules.api_routes import router as api_router
from modules.web_routes import router as web_router

app = FastAPI(title=APP_NAME, version=APP_VERSION)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Create storage directories
os.makedirs("storage/videos", exist_ok=True)
os.makedirs("storage/playlists", exist_ok=True)

# Health check endpoint for Render
@app.get("/health")
async def health_check():
    """Health check endpoint for deployment monitoring"""
    return {
        "status": "healthy",
        "app": APP_NAME,
        "version": APP_VERSION
    }

# Include routers
app.include_router(api_router)
app.include_router(web_router)

if __name__ == "__main__":
    import uvicorn
    print("🎬 TikTok CDN Demo")
    print("⚠️  Educational demonstration only")
    print(f"🌐 http://localhost:{PORT}")
    uvicorn.run("main:app", host=HOST, port=PORT, reload=True)
