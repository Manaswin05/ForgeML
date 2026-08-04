from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from api.routes import router
from config import API_TITLE, API_VERSION, API_DESCRIPTION
import uvicorn
import sys

# Initialize FastAPI app
app = FastAPI(
    title=API_TITLE,
    version=API_VERSION,
    description=API_DESCRIPTION
)

# Add CORS middleware — allow React dev server (5173) and any other origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"],
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

# Auto-run server when script is executed directly
if __name__ == "__main__":
    print("🔥 Starting ForgeML API Server...")
    print("🌐 API available at: http://localhost:8000")
    print("📖 API docs: http://localhost:8000/docs")
    print("⚛️  Start the React frontend: cd frontend && npm run dev")
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