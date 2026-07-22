import pandas as pd
from pathlib import Path
from typing import Tuple, Dict, Any

class DatasetLoader:
    """Handles CSV dataset loading and initial validation."""
    
    @staticmethod
    def load_csv(file_path: str) -> pd.DataFrame:
        """Load CSV file and return DataFrame."""
        try:
            df = pd.read_csv(file_path)
            if df.empty:
                raise ValueError("Dataset is empty")
            return df
        except Exception as e:
            raise Exception(f"Error loading CSV: {str(e)}")
    
    @staticmethod
    def get_dataset_info(df: pd.DataFrame) -> Dict[str, Any]:
        """Get basic dataset information."""
        return {
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": df.columns.tolist(),
            "data_types": df.dtypes.astype(str).to_dict(),
            "memory_usage_mb": df.memory_usage(deep=True).sum() / 1024**2
        }
    
    @staticmethod
    def get_preview(df: pd.DataFrame, n_rows: int = 10) -> Dict[str, Any]:
        """Get first n rows as dictionary."""
        return df.head(n_rows).to_dict(orient="records")
