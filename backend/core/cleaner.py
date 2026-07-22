import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, OneHotEncoder
from typing import Dict, Any, List
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib

class DataCleaner:
    """Handles data cleaning and preprocessing operations."""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.pipeline = None
        self.scaler = None
        self.encoder = None
        self.numeric_cols = self._get_numeric_cols()
        self.categorical_cols = self._get_categorical_cols()
    
    def _get_numeric_cols(self) -> List[str]:
        """Get numeric columns."""
        return self.df.select_dtypes(include=[np.number]).columns.tolist()
    
    def _get_categorical_cols(self) -> List[str]:
        """Get categorical columns."""
        return self.df.select_dtypes(exclude=[np.number]).columns.tolist()
    
    def drop_missing_values(self) -> pd.DataFrame:
        """Drop rows with any missing values."""
        self.df = self.df.dropna()
        return self.df
    
    def fill_numeric_mean(self) -> pd.DataFrame:
        """Fill missing numeric values with mean."""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        self.df[numeric_cols] = self.df[numeric_cols].fillna(self.df[numeric_cols].mean())
        return self.df
    
    def fill_numeric_median(self) -> pd.DataFrame:
        """Fill missing numeric values with median."""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        self.df[numeric_cols] = self.df[numeric_cols].fillna(self.df[numeric_cols].median())
        return self.df
    
    def one_hot_encode(self) -> pd.DataFrame:
        """Apply one-hot encoding to categorical columns."""
        categorical_cols = self.df.select_dtypes(exclude=[np.number]).columns.tolist()
        if categorical_cols:
            self.df = pd.get_dummies(self.df, columns=categorical_cols, drop_first=True)
        return self.df
    
    def standard_scale(self) -> pd.DataFrame:
        """Apply standard scaling to numeric columns."""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            scaler = StandardScaler()
            self.df[numeric_cols] = scaler.fit_transform(self.df[numeric_cols])
            self.scaler = scaler
        return self.df
    
    def normalize(self) -> pd.DataFrame:
        """Apply min-max normalization to numeric columns."""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            scaler = MinMaxScaler()
            self.df[numeric_cols] = scaler.fit_transform(self.df[numeric_cols])
            self.scaler = scaler
        return self.df
    
    def apply_cleaning_pipeline(self, operations: Dict[str, bool]) -> pd.DataFrame:
        """Apply multiple cleaning operations in sequence."""
        if operations.get("drop_missing_values"):
            self.drop_missing_values()
        
        if operations.get("fill_numeric_mean"):
            self.fill_numeric_mean()
        
        if operations.get("fill_numeric_median"):
            self.fill_numeric_median()
        
        if operations.get("one_hot_encode"):
            self.one_hot_encode()
        
        if operations.get("standard_scale"):
            self.standard_scale()
        
        if operations.get("normalize"):
            self.normalize()
        
        return self.df
    
    def get_cleaned_data(self) -> pd.DataFrame:
        """Return cleaned DataFrame."""
        return self.df
    
    def save_cleaning_config(self, filepath: str, operations: Dict[str, bool]):
        """Save cleaning configuration for later use."""
        config = {
            "operations": operations,
            "scaler": self.scaler,
            "encoder": self.encoder
        }
        joblib.dump(config, filepath)
    
    @staticmethod
    def load_cleaning_config(filepath: str) -> Dict[str, Any]:
        """Load cleaning configuration."""
        return joblib.load(filepath)
