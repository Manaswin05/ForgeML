from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from api.routes import router
from config import API_TITLE, API_VERSION, API_DESCRIPTION
import uvicorn
import sys
import os

# Initialize FastAPI app
app = FastAPI(
    title=API_TITLE,
    version=API_VERSION,
    description=API_DESCRIPTION
)

# Add CORS middleware — allow all origins in production, specific origins in development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "ForgeML API is running!"}

# Mount static files directory (for frontend build)
static_dir = Path(__file__).parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Serve frontend index.html for all non-API routes
@app.get("/")
async def serve_frontend():
    index_path = static_dir / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return {"message": "Frontend not built. Run 'npm run build' in frontend directory."}

@app.get("/{full_path:path}")
async def catch_all(full_path: str):
    # Check if it's an API route
    if full_path.startswith("api/"):
        return {"error": "Not found"}, 404
    
    # Serve frontend files
    file_path = static_dir / full_path
    if file_path.exists() and file_path.is_file():
        return FileResponse(file_path)
    
    # Fall back to index.html for client-side routing
    index_path = static_dir / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    
    return {"error": "Not found"}, 404

# Auto-run server when script is executed directly
if __name__ == "__main__":
    print("🔥 Starting ForgeML API Server...")
    print("🌐 API available at: http://localhost:8000")
    print("📖 API docs: http://localhost:8000/docs")
    print("⚛️  Frontend available at: http://localhost:8000")
    print("Press Ctrl+C to stop the server")
    print("-" * 50)

    try:
        uvicorn.run(
            "app:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            reload_dirs=["."],
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 ForgeML server stopped")
        sys.exit(0)