import pandas as pd
import numpy as np
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, mean_absolute_error, mean_squared_error, r2_score
)
from typing import Dict, Any

class ModelEvaluator:
    """Evaluates model performance."""
    
    @staticmethod
    def evaluate_classification(model, X_test: pd.DataFrame, y_test: pd.Series) -> Dict[str, Any]:
        """Evaluate classification model."""
        y_pred = model.predict(X_test)
        
        # Handle binary vs multi-class
        average = 'binary' if len(np.unique(y_test)) == 2 else 'weighted'
        
        metrics = {
            "accuracy": float(accuracy_score(y_test, y_pred)),
            "precision": float(precision_score(y_test, y_pred, average=average, zero_division=0)),
            "recall": float(recall_score(y_test, y_pred, average=average, zero_division=0)),
            "f1_score": float(f1_score(y_test, y_pred, average=average, zero_division=0)),
        }
        
        # Add confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        metrics["confusion_matrix"] = cm.tolist()
        
        return metrics
    
    @staticmethod
    def evaluate_regression(model, X_test: pd.DataFrame, y_test: pd.Series) -> Dict[str, Any]:
        """Evaluate regression model."""
        y_pred = model.predict(X_test)
        
        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, y_pred)
        
        metrics = {
            "mae": float(mae),
            "mse": float(mse),
            "rmse": float(rmse),
            "r2_score": float(r2)
        }
        
        return metrics
    
    @staticmethod
    def evaluate(model, X_test: pd.DataFrame, y_test: pd.Series, task_type: str) -> Dict[str, Any]:
        """Unified evaluation function."""
        if task_type == 'classification':
            return ModelEvaluator.evaluate_classification(model, X_test, y_test)
        else:
            return ModelEvaluator.evaluate_regression(model, X_test, y_test)
