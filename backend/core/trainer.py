import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression, LinearRegression, Ridge, Lasso
from sklearn.model_selection import train_test_split
from typing import Dict, Any, Tuple
from config import RANDOM_STATE, TEST_SIZE

class ModelTrainer:
    """Handles model training with multiple algorithm support."""
    
    CLASSIFICATION_MODELS = {
        "random_forest": RandomForestClassifier,
        "knn": KNeighborsClassifier,
        "naive_bayes": GaussianNB,
        "logistic_regression": LogisticRegression
    }
    
    REGRESSION_MODELS = {
        "random_forest": RandomForestRegressor,
        "knn": KNeighborsRegressor,
        "linear_regression": LinearRegression,
        "ridge_regression": Ridge,
        "lasso_regression": Lasso
    }
    
    def __init__(self, df: pd.DataFrame, target_col: str, feature_cols: list, test_size: float = TEST_SIZE):
        self.df = df
        self.target_col = target_col
        self.feature_cols = feature_cols
        self.test_size = test_size
        self.X = None
        self.y = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.model = None
        self.task_type = None
        self._prepare_data()
    
    def _prepare_data(self):
        """Prepare X and y for training."""
        self.X = self.df[self.feature_cols]
        self.y = self.df[self.target_col]
        
        # Detect task type (classification vs regression)
        if self.y.dtype == 'object' or self.y.nunique() < 10:
            self.task_type = 'classification'
        else:
            self.task_type = 'regression'
        
        # Train-test split
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=self.test_size, random_state=RANDOM_STATE
        )
    
    def train(
        self,
        model_type: str = "random_forest",
        **hyperparams
    ) -> Dict[str, Any]:
        """Train model with given hyperparameters."""
        
        if self.task_type == 'classification':
            if model_type not in self.CLASSIFICATION_MODELS:
                raise ValueError(f"Unknown classification model: {model_type}")
            ModelClass = self.CLASSIFICATION_MODELS[model_type]
        else:
            if model_type not in self.REGRESSION_MODELS:
                raise ValueError(f"Unknown regression model: {model_type}")
            ModelClass = self.REGRESSION_MODELS[model_type]
        
        # Filter hyperparams to valid ones for the model
        valid_params = {}
        try:
            model_instance = ModelClass()
            valid_param_names = model_instance.get_params().keys()
            valid_params = {k: v for k, v in hyperparams.items() if k in valid_param_names}
        except:
            pass
        
        # Train
        self.model = ModelClass(**valid_params)
        self.model.fit(self.X_train, self.y_train)
        
        return {
            "status": "success",
            "task_type": self.task_type,
            "model_type": model_type,
            "train_set_size": len(self.X_train),
            "test_set_size": len(self.X_test)
        }
    
    def get_model(self):
        """Return trained model."""
        return self.model
    
    def get_test_data(self) -> Tuple[pd.DataFrame, pd.Series]:
        """Return test data."""
        return self.X_test, self.y_test
