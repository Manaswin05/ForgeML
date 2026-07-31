from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class DatasetInfo(BaseModel):
    """Dataset information response."""
    rows: int
    columns: int
    column_names: List[str]
    data_types: Dict[str, str]
    memory_usage_mb: float

class DatasetProfile(BaseModel):
    """Complete dataset profile."""
    rows: int
    columns: int
    column_names: List[str]
    data_types: Dict[str, str]
    descriptive_stats: Dict[str, Any]
    missing_values: Dict[str, int]
    duplicates: int
    memory_usage_mb: float
    column_statistics: Dict[str, Any]
    correlation_matrix: Dict[str, Dict[str, float]]

class TrainingRequest(BaseModel):
    """Request for model training."""
    target_column: str
    feature_columns: List[str]
    model_type: str = "random_forest"
    model_name: str = None  # Custom model name (optional)
    cleaning_operations: Dict[str, bool]
    hyperparameters: Dict[str, Any] = {}
    test_size: float = 0.2

class TrainingResponse(BaseModel):
    """Response from model training."""
    status: str
    task_type: str
    model_type: str
    metrics: Dict[str, Any]
    train_set_size: int
    test_set_size: int

class PredictionRequest(BaseModel):
    """Request for prediction."""
    data: Dict[str, Any]

class PredictionResponse(BaseModel):
    """Response from prediction."""
    prediction: Any
    confidence: Optional[float] = None

class ModelExportResponse(BaseModel):
    """Response from model export."""
    status: str
    filepath: str
    filename: str

class ErrorResponse(BaseModel):
    """Error response."""
    error: str
    detail: Optional[str] = None

class AnalysisRequest(BaseModel):
    """Request for dataset analysis."""
    target_column: str
    feature_columns: List[str]

class DatasetLoadRequest(BaseModel):
    """Request to load dataset from URL."""
    url: str
