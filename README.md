<div align="center">

# 🔥 ForgeML

### Forge Machine Learning Workflows Effortlessly

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-00a393.svg)](https://fastapi.tiangolo.com)
[![scikit-learn](https://img.shields.io/badge/sklearn-1.3+-f89a36.svg)](https://scikit-learn.org)

**A powerful no-code machine learning platform that lets you build, train, and deploy ML models through an intuitive web interface.**

# ForgeML - Version 1.3.4

<div align="center">

[Quick Start](#-quick-start) • [Features](#-features) • [API Reference](#-api-reference) • [Documentation](#-documentation)

</div>

---

## 🚀 Quick Start (New & Improved!)

### Option 1: One-Command Setup & Run
```bash
# Install dependencies and start server
python run.py setup

# Or use the batch file on Windows
run.bat setup
```

### Option 2: Individual Commands
```bash
# Just start the server (if dependencies already installed)
python run.py dev

# Or simply:
run.bat

# Or use make (if available):
make dev
```

### Option 3: Traditional Method
```bash
cd backend
python app.py
```

## 🛠️ All Available Commands

### Using run.py:
```bash
python run.py dev      # Start development server (default)
python run.py prod     # Start production server  
python run.py setup    # Install dependencies
python run.py test     # Run all tests
python run.py clean    # Clean cache files
python run.py reset    # Reset models and uploads
```

### Using batch file (Windows):
```bash
run.bat           # Start dev server
run.bat setup     # Install dependencies
run.bat test      # Run tests
```

### Using Makefile:
```bash
make              # Start dev server
make setup        # Install dependencies
make test         # Run tests
make clean        # Clean cache
make reset        # Reset data
```

The application will be available at: **http://localhost:8000**
API docs will be available at: **http://localhost:8000/docs**

## ✨ Features

- **Integrated Dataset Store (New in v1.3!)**: Browse and load massive datasets directly from OpenML. Includes external deep-links to query Kaggle, Google Dataset Search, and GitHub Repositories.
- **Easy Setup**: One command to install and run
- **Auto-Reload**: Development server automatically reloads on code changes
- **Health Check**: Built-in health endpoint at `/health`
- **Better Logging**: Improved logging with timestamps
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Multiple Run Options**: Python script, batch file, or Makefile

## 🛠️ Development Workflow

1. **First Time Setup:**
   ```bash
   python run.py setup
   ```

2. **Daily Development:**
   ```bash
   python run.py dev    # Starts server with auto-reload
   ```

3. **Testing:**
   ```bash
   python run.py test   # Run all API tests
   ```

4. **Cleaning:**
   ```bash
   python run.py clean  # Remove cache files
   python run.py reset  # Reset models and uploads
   ```

## 📊 How to Use the ML Platform

### Step 1: Upload Dataset
1. Open http://localhost:8000 in your browser
2. Upload a CSV file
3. Review dataset statistics and preview

### Step 2: Train Model
1. Click "Proceed to Training"
2. Select target column (Y)
3. Select feature columns (X)
4. Choose data cleaning options
5. Select model type (Random Forest, KNN, Naive Bayes, Logistic Regression)
6. Configure hyperparameters (optional)
7. Click "Train Model"

### Step 3: Evaluate & Export
1. Review training metrics
2. Click "Download Model (.joblib)" to save the trained model

## 🔧 Configuration

Copy `.env.example` to `.env` to customize settings:
```bash
cp .env.example .env
```

## 📁 Project Structure

```
ForgeML/
├── run.py              # Main run script
├── run.bat            # Windows batch file
├── Makefile           # Make commands
├── package.json       # npm-style scripts
├── backend/           # FastAPI backend
│   ├── app.py        # Main application (auto-runs server)
│   ├── config.py     # Configuration
│   ├── api/          # API routes
│   └── core/         # ML logic
├── docs/             # Documentation
└── tests/            # Test files
```

## 🚨 Troubleshooting

### Dependencies Issues:
```bash
python run.py setup    # Reinstall dependencies
```

### Port Already in Use:
The server will show an error if port 8000 is busy. Stop other services or change the port in `config.py`.

### Cache Issues:
```bash
python run.py clean    # Clear Python cache
```

## 🧪 Testing

Run all tests:
```bash
python run.py test
```

Individual test files:
```bash
python test_api.py
python test_weather_api.py
python test_predict.py
```

### Dataset Management
- `POST /api/upload` - Upload CSV file
- `GET /api/profile` - Get dataset profile (statistics, missing values, etc.)

### Model Training
- `POST /api/train` - Train model with specified configuration
- `POST /api/predict` - Make predictions using trained model
- `POST /api/export` - Export trained model
- `GET /api/download/{filename}` - Download exported model file

### Health Check
- `GET /api/health` - Check API status

## Project Structure

```
forgeml/
├── backend/
│   ├── app.py                      # FastAPI application
│   ├── config.py                   # Configuration settings
│   ├── requirements.txt            # Python dependencies
│   ├── core/
│   │   ├── loader.py               # Dataset loading
│   │   ├── profiler.py             # Dataset statistics
│   │   ├── cleaner.py              # Data preprocessing
│   │   ├── trainer.py              # Model training
│   │   ├── evaluator.py            # Model evaluation
│   │   └── exporter.py             # Model export
│   ├── api/
│   │   ├── routes.py               # API endpoints
│   │   └── schemas.py              # Pydantic models
│   ├── templates/
│   │   ├── base.html               # Base template
│   │   ├── home.html               # Upload page
│   │   └── train.html              # Training page
│   ├── static/
│   │   └── style.css               # Custom styles
│   ├── uploads/                    # Uploaded files
│   ├── models/                     # Exported models
│   └── reports/                    # Training reports
└── README.md
```

## Supported Models

### Classification
- Random Forest Classifier
- K-Nearest Neighbors (KNN)
- Naive Bayes
- Logistic Regression

### Regression
- Random Forest Regressor
- K-Nearest Neighbors (KNN)
- Linear Regression

## Data Cleaning Options

- **Drop Missing Values** - Remove rows with any missing values
- **Fill Mean** - Fill numeric missing values with mean
- **Fill Median** - Fill numeric missing values with median
- **One-Hot Encode** - Encode categorical columns
- **Standard Scale** - Normalize numeric features
- **Normalize** - Min-max normalization

## Classification Metrics

- Accuracy
- Precision
- Recall
- F1 Score
- Confusion Matrix

## Regression Metrics

- Mean Absolute Error (MAE)
- Mean Squared Error (MSE)
- Root Mean Squared Error (RMSE)
- R² Score

## Sample Dataset

To test, you can use a sample CSV like:

```csv
Age,Salary,Gender,Purchased
25,35000,Male,0
32,45000,Female,1
28,38000,Male,0
45,65000,Male,1
```

## Troubleshooting

### Port Already in Use
If port 8000 is already in use, modify the port in `app.py`:
```python
uvicorn.run("app:app", host="0.0.0.0", port=8001)  # Change to 8001
```

### Import Errors
Ensure you're in the `backend` directory and have installed all dependencies:
```bash
pip install -r requirements.txt
```

### Template Not Found
Make sure the `templates/` directory exists in the backend folder.

## Future Enhancements (Phase 2+)

- Multiple model comparison
- Hyperparameter tuning
- API generation (`/predict`)
- Model explainability (SHAP/LIME)
- Experiment tracking
- Docker deployment
- Cloud integration

## License

MIT License

## Support

For issues or questions, please refer to the PRD.md file for detailed specifications.
#
