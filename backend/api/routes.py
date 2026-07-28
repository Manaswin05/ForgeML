from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import pandas as pd
import os
from pathlib import Path
from typing import Dict, Any
import joblib
import logging
import io

from core.loader import DatasetLoader
from core.profiler import DatasetProfiler
from core.cleaner import DataCleaner
from core.trainer import ModelTrainer
from core.evaluator import ModelEvaluator
from core.exporter import ModelExporter
from core.analyzer import DatasetAnalyzer
from api.schemas import (
    DatasetInfo, DatasetProfile, TrainingRequest, TrainingResponse,
    PredictionRequest, PredictionResponse, ModelExportResponse, ErrorResponse, AnalysisRequest
)
from config import DATASETS_DIR, MODELS_DIR

# Set up logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["ForgeML API"])

# Global storage for current session
current_session = {
    "df": None,
    "model": None,
    "model_type": None,
    "model_name": None,  # Custom model name
    "task_type": None,
    "feature_cols": None,
    "target_col": None,
    "preprocessing_pipeline": None,
    "X_test": None,
    "y_test": None
}

@router.get("/status")
async def get_status():
    """Get current session status."""
    try:
        has_data = current_session["df"] is not None
        has_model = current_session["model"] is not None
        
        return {
            "status": "ready",
            "has_data": has_data,
            "has_model": has_model,
            "data_rows": len(current_session["df"]) if has_data else 0,
            "model_type": current_session.get("model_type"),
            "task_type": current_session.get("task_type")
        }
    except Exception as e:
        logger.error(f"Error getting status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/reset")
def reset_session():
    """Reset the current session data."""
    try:
        for key in current_session:
            current_session[key] = None
        return {"status": "success", "message": "Session reset successfully"}
    except Exception as e:
        logger.error(f"Error resetting session: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload")
async def upload_dataset(file: UploadFile = File(...)):
    """Upload and load CSV dataset."""
    try:
        logger.info(f"Uploading file: {file.filename}")
        
        # Validate file type
        if not file.filename.endswith(('.csv', '.xlsx')):
            raise HTTPException(status_code=400, detail="Only CSV and Excel files are supported")
        
        # Read into memory
        content = await file.read()
        file_obj = io.BytesIO(content)
        
        # Load dataset
        df = DatasetLoader.load_csv(file_obj)
        current_session["df"] = df
        
        # Get info
        info = DatasetLoader.get_dataset_info(df)
        preview = DatasetLoader.get_preview(df)
        
        logger.info(f"Dataset loaded successfully: {info['rows']} rows, {info['columns']} columns")
        
        return {
            "status": "success",
            "info": info,
            "preview": preview
        }
    except Exception as e:
        logger.error(f"Error uploading dataset: {e}")
        raise HTTPException(status_code=500, detail=f"Error uploading dataset: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/profile")
def get_dataset_profile():
    """Get complete dataset profile."""
    try:
        if current_session["df"] is None:
            raise ValueError("No dataset loaded")
        
        import json
        profile = DatasetProfiler.get_full_profile(current_session["df"])
        
        # Ensure all values are JSON-serializable
        def clean_dict(d):
            if isinstance(d, dict):
                return {k: clean_dict(v) for k, v in d.items()}
            if isinstance(d, list):
                return [clean_dict(v) for v in d]
            if isinstance(d, float):
                if d != d or d == float('inf') or d == float('-inf'):  # NaN or inf
                    return None
            return d
        
        profile = clean_dict(profile)
        return profile
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/train")
def train_model(request: TrainingRequest):
    """Train a model."""
    try:
        if current_session["df"] is None:
            raise ValueError("No dataset loaded")
        
        df = current_session["df"].copy()
        
        # Validate inputs
        if request.target_column not in df.columns:
            raise ValueError(f"Target column '{request.target_column}' not found")
        
        for col in request.feature_columns:
            if col not in df.columns:
                raise ValueError(f"Feature column '{col}' not found")
        
        if request.target_column in request.feature_columns:
            raise ValueError("Target cannot be in feature columns")
        
        if len(request.feature_columns) == 0:
            raise ValueError("At least one feature column required")
        
        # Select target and features before cleaning to avoid dropping other columns accidentally
        selected_cols = request.feature_columns + [request.target_column]
        df = df[selected_cols].copy()
        
        # Apply cleaning
        cleaner = DataCleaner(df)
        df = cleaner.apply_cleaning_pipeline(request.cleaning_operations)
        
        # Since features might have been one-hot encoded or renamed, get the new feature columns
        new_feature_cols = [c for c in df.columns if c != request.target_column]
        
        # Train model
        trainer = ModelTrainer(df, request.target_column, new_feature_cols, test_size=request.test_size)
        trainer.train(request.model_type, **request.hyperparameters)
        
        # Evaluate
        X_test, y_test = trainer.get_test_data()
        metrics = ModelEvaluator.evaluate(
            trainer.get_model(),
            X_test,
            y_test,
            trainer.task_type
        )
        
        # Store in session
        current_session["model"] = trainer.get_model()
        current_session["model_type"] = request.model_type
        current_session["model_name"] = request.model_name  # Store custom name
        current_session["task_type"] = trainer.task_type
        current_session["feature_cols"] = new_feature_cols
        current_session["original_feature_cols"] = request.feature_columns
        current_session["target_col"] = request.target_column
        current_session["preprocessing_pipeline"] = cleaner
        current_session["X_test"] = X_test
        current_session["y_test"] = y_test
        
        return {
            "status": "success",
            "task_type": trainer.task_type,
            "model_type": request.model_type,
            "metrics": metrics,
            "train_set_size": len(trainer.X_train),
            "test_set_size": len(trainer.X_test)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/predict")
def predict(request: PredictionRequest):
    """Make prediction using trained model."""
    try:
        if current_session["model"] is None:
            raise ValueError("No trained model available")
        
        # Convert input to dataframe
        input_df = pd.DataFrame([request.data])
        
        # Make prediction
        model = current_session["model"]
        
        # Ensure column order matches feature_cols if available
        if current_session.get("feature_cols"):
            for col in current_session["feature_cols"]:
                if col not in input_df.columns:
                    input_df[col] = 0
            input_df = input_df[current_session["feature_cols"]]
            
        prediction = model.predict(input_df)[0]
        
        # Get confidence for classification
        confidence = None
        if hasattr(model, 'predict_proba'):
            proba = model.predict_proba(input_df)[0]
            confidence = float(max(proba))
            
        # Convert prediction to native python type
        if hasattr(prediction, 'item'):
            prediction = prediction.item()
        
        return {
            "status": "200 OK",
            "prediction": float(prediction) if isinstance(prediction, (int, float)) else str(prediction),
            "confidence": confidence
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/upload_model")
async def upload_model(file: UploadFile = File(...)):
    """Upload a trained model (.pkl)."""
    try:
        if not file.filename.endswith('.pkl'):
            raise HTTPException(status_code=400, detail="Only .pkl files are supported")
        
        # Read into memory
        content = await file.read()
        file_obj = io.BytesIO(content)
        
        # Load model
        model = joblib.load(file_obj)
        
        current_session["model"] = model
        current_session["model_name"] = file.filename
        
        # Attempt to load metadata if exists
        metadata_path = MODELS_DIR / f"{file.filename}.metadata.json"
        if metadata_path.exists():
            import json
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
                current_session["task_type"] = metadata.get("task_type")
                current_session["feature_cols"] = metadata.get("feature_columns")
                current_session["model_type"] = metadata.get("model_type")
                
        return {"status": "success", "message": "Model loaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/export")
def export_model():
    """Export trained model in pickle format."""
    try:
        if current_session["model"] is None:
            raise ValueError("No trained model available")
        
        model = current_session["model"]
        
        # Use custom model name if provided, otherwise auto-generate
        if current_session.get("model_name"):
            # Sanitize custom name (remove special characters)
            custom_name = "".join(c for c in current_session["model_name"] if c.isalnum() or c in '_-')
            filename = f"{custom_name}.pkl"
        else:
            # Auto-generate filename
            filename = f"forgeml_model_{current_session['model_type']}.pkl"
        
        filepath = MODELS_DIR / filename
        
        # Save model using ModelExporter (pickle format with compression)
        ModelExporter.save_model(model, str(filepath), compress=True)
        
        # Save metadata
        metadata = {
            "model_type": current_session["model_type"],
            "task_type": current_session["task_type"],
            "feature_columns": current_session["feature_cols"],
            "target_column": current_session["target_col"],
            "custom_name": current_session.get("model_name", ""),
            "export_format": "pickle",
            "compressed": True
        }
        metadata_path = str(filepath).replace('.pkl', '.pkl.metadata.json')
        ModelExporter.save_metadata(metadata, metadata_path)
        
        return {
            "status": "success",
            "filepath": str(filepath),
            "filename": filename
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/download/{filename}")
def download_model(filename: str):
    """Download exported model file."""
    try:
        filepath = MODELS_DIR / filename
        if not filepath.exists():
            raise ValueError("Model file not found")
        
        return FileResponse(filepath, filename=filename)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/model-metadata/{filename}")
def get_model_metadata(filename: str):
    """Get model metadata."""
    try:
        metadata_path = MODELS_DIR / f"{filename}.metadata.json"
        if not metadata_path.exists():
            raise ValueError(f"Metadata not found for {filename}")
        
        import json
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        
        return metadata
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/analysis")
def generate_analysis(request: AnalysisRequest):
    """Generate dataset analysis including plots and model comparisons."""
    try:
        if current_session["df"] is None:
            raise ValueError("No dataset loaded")
            
        df = current_session["df"].copy()
        
        # Validate inputs
        if not request.feature_columns:
            raise ValueError("Feature columns list cannot be empty")
            
        if request.target_column in request.feature_columns:
            raise ValueError("Target column cannot be included in feature columns")

        if request.target_column not in df.columns:
            raise ValueError(f"Target column '{request.target_column}' not found")
            
        for col in request.feature_columns:
            if col not in df.columns:
                raise ValueError(f"Feature column '{col}' not found")
                
        # Get plots
        corr_matrix = DatasetAnalyzer.get_correlation_matrix(df, request.feature_columns + [request.target_column])
        pairplot = DatasetAnalyzer.get_pairplot(df, request.feature_columns, request.target_column)
        boxplots = DatasetAnalyzer.get_boxplots(df, request.feature_columns, request.target_column)
        
        # Get model comparisons
        model_comparisons = DatasetAnalyzer.compare_models(df, request.feature_columns, request.target_column)
        
        return {
            "status": "success",
            "correlation_matrix": corr_matrix,
            "pairplot": pairplot,
            "boxplots": boxplots,
            "model_comparisons": model_comparisons
        }
    except Exception as e:
        logger.error(f"Error in analysis: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "ok"}
