from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pathlib import Path
from api.routes import router
from config import CORS_ORIGINS, API_TITLE, API_VERSION, API_DESCRIPTION
import joblib
import pandas as pd
import uvicorn
import sys

# Initialize FastAPI app
app = FastAPI(
    title=API_TITLE,
    version=API_VERSION,
    description=API_DESCRIPTION
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)

# Setup paths — serve from backend/templates and backend/static
BASE_DIR = Path(__file__).parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

# ── Page Routes (registered BEFORE static mount) ──────────────────

@app.get("/", response_class=HTMLResponse)
async def index():
    """Serve main dashboard page."""
    try:
        index_path = TEMPLATES_DIR / "index.html"
        if not index_path.exists():
            raise FileNotFoundError(f"Index file not found: {index_path}")
        
        with open(index_path, "r", encoding="utf-8") as f:
            content = f.read()
        return content
    except Exception as e:
        return f"<h1>Error loading page</h1><p>{str(e)}</p>"

@app.get("/train", response_class=HTMLResponse)
async def train_page():
    """Serve model training configuration page."""
    try:
        train_path = TEMPLATES_DIR / "train.html"
        if not train_path.exists():
            raise FileNotFoundError(f"Train page not found: {train_path}")
        
        with open(train_path, "r", encoding="utf-8") as f:
            content = f.read()
        return content
    except Exception as e:
        return f"<h1>Error loading page</h1><p>{str(e)}</p>"

@app.get("/predict_ui", response_class=HTMLResponse)
async def predict_page():
    """Serve prediction page."""
    try:
        predict_path = TEMPLATES_DIR / "predict.html"
        if not predict_path.exists():
            raise FileNotFoundError(f"Predict page not found: {predict_path}")
        
        with open(predict_path, "r", encoding="utf-8") as f:
            content = f.read()
        return content
    except Exception as e:
        return f"<h1>Error loading page</h1><p>{str(e)}</p>"

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "ForgeML is running!"}

# ── Mount static files (AFTER page routes) ────────────────────────
try:
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
except Exception as e:
    print(f"Error mounting static files: {e}")
    raise

# Auto-run server when script is executed directly
if __name__ == "__main__":
    print("🔥 Starting ForgeML Development Server...")
    print("🌐 Open your browser to: http://localhost:8000")
    print("📖 API documentation: http://localhost:8000/docs")
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