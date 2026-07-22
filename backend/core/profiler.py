import pandas as pd
import numpy as np
from typing import Dict, Any
import json

class DatasetProfiler:
    """Generates detailed dataset statistics and insights."""
    
    @staticmethod
    def _make_json_serializable(value):
        """Convert numpy/pandas types to JSON-serializable types."""
        if pd.isna(value):
            return None
        if isinstance(value, (np.integer, np.floating)):
            if np.isinf(value) or np.isnan(value):
                return None
            return float(value)
        if isinstance(value, dict):
            return {k: DatasetProfiler._make_json_serializable(v) for k, v in value.items()}
        if isinstance(value, list):
            return [DatasetProfiler._make_json_serializable(v) for v in value]
        return value
    
    @staticmethod
    def get_descriptive_stats(df: pd.DataFrame) -> Dict[str, Any]:
        """Get df.describe() as dictionary."""
        stats = df.describe().to_dict()
        return DatasetProfiler._make_json_serializable(stats)
    
    @staticmethod
    def get_missing_values(df: pd.DataFrame) -> Dict[str, int]:
        """Get count of missing values per column."""
        return {k: int(v) for k, v in df.isnull().sum().to_dict().items()}
    
    @staticmethod
    def get_duplicate_count(df: pd.DataFrame) -> int:
        """Get total duplicate row count."""
        return int(df.duplicated().sum())
    
    @staticmethod
    def get_memory_usage(df: pd.DataFrame) -> Dict[str, float]:
        """Get memory usage per column in MB."""
        memory_usage = (df.memory_usage(deep=True) / 1024**2).to_dict()
        return {k: round(float(v), 4) for k, v in memory_usage.items()}
    
    @staticmethod
    def get_column_statistics(df: pd.DataFrame) -> Dict[str, Any]:
        """Get per-column statistics."""
        stats = {}
        for col in df.columns:
            if pd.api.types.is_numeric_dtype(df[col]):
                col_min = df[col].min()
                col_max = df[col].max()
                col_mean = df[col].mean()
                col_std = df[col].std()
                
                # Handle NaN and inf values
                stats[col] = {
                    "type": "numeric",
                    "min": float(col_min) if pd.notna(col_min) and not np.isinf(col_min) else None,
                    "max": float(col_max) if pd.notna(col_max) and not np.isinf(col_max) else None,
                    "mean": float(col_mean) if pd.notna(col_mean) and not np.isinf(col_mean) else None,
                    "std": float(col_std) if pd.notna(col_std) and not np.isinf(col_std) else None,
                    "missing": int(df[col].isnull().sum())
                }
            else:
                stats[col] = {
                    "type": "categorical",
                    "unique_values": int(df[col].nunique()),
                    "missing": int(df[col].isnull().sum())
                }
        return stats
    
    @staticmethod
    def get_correlation_matrix(df: pd.DataFrame) -> Dict[str, Dict[str, float]]:
        """Get correlation matrix for numeric columns."""
        numeric_df = df.select_dtypes(include=[np.number])
        if numeric_df.empty:
            return {}
        corr = numeric_df.corr().to_dict()
        return DatasetProfiler._make_json_serializable(corr)
    
    @staticmethod
    def get_full_profile(df: pd.DataFrame) -> Dict[str, Any]:
        """Get complete dataset profile."""
        return {
            "rows": len(df),
            "columns": len(df.columns),
            "column_names": df.columns.tolist(),
            "data_types": {k: str(v) for k, v in df.dtypes.to_dict().items()},
            "descriptive_stats": DatasetProfiler.get_descriptive_stats(df),
            "missing_values": DatasetProfiler.get_missing_values(df),
            "duplicates": DatasetProfiler.get_duplicate_count(df),
            "memory_usage_mb": round(float(df.memory_usage(deep=True).sum()) / 1024**2, 4),
            "column_statistics": DatasetProfiler.get_column_statistics(df),
            "correlation_matrix": DatasetProfiler.get_correlation_matrix(df)
        }
