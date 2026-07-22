import pickle
import json
import gzip
from pathlib import Path
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class ModelExporter:
    """Handles model export and metadata saving using pickle format."""
    
    @staticmethod
    def save_model(model, filepath: str, compress: bool = True):
        """Save trained model to pickle file with optional compression."""
        try:
            # Ensure filepath has .pkl extension
            if not filepath.endswith('.pkl'):
                filepath = filepath.replace('.joblib', '.pkl') if '.joblib' in filepath else filepath + '.pkl'
            
            if compress:
                # Use gzip compression for smaller files
                with gzip.open(filepath, 'wb') as f:
                    pickle.dump(model, f, protocol=pickle.HIGHEST_PROTOCOL)
            else:
                # Standard pickle without compression
                with open(filepath, 'wb') as f:
                    pickle.dump(model, f, protocol=pickle.HIGHEST_PROTOCOL)
            
            logger.info(f"Model saved successfully to {filepath}")
            return {"status": "success", "filepath": filepath, "compressed": compress}
            
        except Exception as e:
            logger.error(f"Error saving model: {e}")
            raise Exception(f"Failed to save model: {str(e)}")
    
    @staticmethod
    def load_model(filepath: str):
        """Load model from pickle file (handles both compressed and uncompressed)."""
        try:
            # Ensure filepath has .pkl extension
            if not filepath.endswith('.pkl'):
                filepath = filepath.replace('.joblib', '.pkl') if '.joblib' in filepath else filepath + '.pkl'
            
            # Try to load as compressed first
            try:
                with gzip.open(filepath, 'rb') as f:
                    model = pickle.load(f)
                logger.info(f"Loaded compressed model from {filepath}")
                return model
            except (gzip.BadGzipFile, OSError):
                # Fall back to uncompressed pickle
                with open(filepath, 'rb') as f:
                    model = pickle.load(f)
                logger.info(f"Loaded uncompressed model from {filepath}")
                return model
                
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise Exception(f"Failed to load model from {filepath}: {str(e)}")
    
    @staticmethod
    def save_metadata(metadata: Dict[str, Any], filepath: str):
        """Save model metadata to JSON."""
        try:
            # Ensure metadata filepath matches model filepath
            if filepath.endswith('.joblib.metadata.json'):
                filepath = filepath.replace('.joblib.metadata.json', '.pkl.metadata.json')
            elif not filepath.endswith('.pkl.metadata.json'):
                filepath = filepath.replace('.pkl', '.pkl.metadata.json') if '.pkl' in filepath else filepath + '.pkl.metadata.json'
            
            with open(filepath, 'w') as f:
                json.dump(metadata, f, indent=2, default=str)
            
            logger.info(f"Metadata saved to {filepath}")
            return {"status": "success", "filepath": filepath}
            
        except Exception as e:
            logger.error(f"Error saving metadata: {e}")
            raise Exception(f"Failed to save metadata: {str(e)}")
    
    @staticmethod
    def load_metadata(filepath: str) -> Dict[str, Any]:
        """Load model metadata from JSON."""
        try:
            # Handle both old and new metadata file naming
            if filepath.endswith('.joblib.metadata.json'):
                filepath = filepath.replace('.joblib.metadata.json', '.pkl.metadata.json')
            elif not filepath.endswith('.pkl.metadata.json'):
                filepath = filepath.replace('.pkl', '.pkl.metadata.json') if '.pkl' in filepath else filepath + '.pkl.metadata.json'
            
            with open(filepath, 'r') as f:
                metadata = json.load(f)
            
            logger.info(f"Metadata loaded from {filepath}")
            return metadata
            
        except Exception as e:
            logger.error(f"Error loading metadata: {e}")
            raise Exception(f"Failed to load metadata from {filepath}: {str(e)}")
    
    @staticmethod
    def export_model_package(model, metadata: Dict[str, Any], output_dir: str, model_name: str = "model", compress: bool = True):
        """Export model and metadata together with pickle format."""
        try:
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            model_path = output_path / f"{model_name}.pkl"
            metadata_path = output_path / f"{model_name}.pkl.metadata.json"
            
            # Add export format info to metadata
            export_metadata = metadata.copy()
            export_metadata.update({
                "export_format": "pickle",
                "compressed": compress,
                "pickle_protocol": pickle.HIGHEST_PROTOCOL,
                "export_timestamp": str(Path(model_path).stat().st_mtime) if model_path.exists() else None
            })
            
            ModelExporter.save_model(model, str(model_path), compress=compress)
            ModelExporter.save_metadata(export_metadata, str(metadata_path))
            
            logger.info(f"Model package exported successfully to {output_path}")
            
            return {
                "status": "success",
                "model_path": str(model_path),
                "metadata_path": str(metadata_path),
                "compressed": compress
            }
            
        except Exception as e:
            logger.error(f"Error exporting model package: {e}")
            raise Exception(f"Failed to export model package: {str(e)}")
    
    @staticmethod
    def migrate_joblib_to_pickle(joblib_path: str, output_path: Optional[str] = None, compress: bool = True):
        """Migrate existing joblib models to pickle format."""
        try:
            import joblib
            
            # Load the joblib model
            model = joblib.load(joblib_path)
            
            # Determine output path
            if output_path is None:
                output_path = joblib_path.replace('.joblib', '.pkl')
            
            # Save as pickle
            ModelExporter.save_model(model, output_path, compress=compress)
            
            # Migrate metadata if it exists
            metadata_joblib_path = joblib_path + '.metadata.json'
            if Path(metadata_joblib_path).exists():
                metadata = ModelExporter.load_metadata(metadata_joblib_path)
                metadata['migrated_from'] = 'joblib'
                metadata['original_path'] = joblib_path
                ModelExporter.save_metadata(metadata, output_path.replace('.pkl', '.pkl.metadata.json'))
            
            logger.info(f"Successfully migrated {joblib_path} to {output_path}")
            
            return {
                "status": "success",
                "original_path": joblib_path,
                "new_path": output_path,
                "compressed": compress
            }
            
        except Exception as e:
            logger.error(f"Error migrating joblib to pickle: {e}")
            raise Exception(f"Failed to migrate {joblib_path}: {str(e)}")
