# 🚀 ForgeML Setup Guide

## Quick Setup (Recommended)

### 1. Clone/Download Project
```bash
# If cloning
git clone <your-repo>
cd ForgeML

# If downloaded, extract and navigate to folder
cd ForgeML
```

### 2. One-Command Setup
```bash
# Install dependencies and start server
python run.py setup
```

That's it! Your server will be running at http://localhost:8000

## Alternative Setup Methods

### Method 1: Python Script
```bash
# Setup dependencies
python run.py setup

# Start development server
python run.py dev
```

### Method 2: Windows Batch File
```bash
# Setup
run.bat setup

# Start server
run.bat
```

### Method 3: Makefile (if available)
```bash
# Setup
make setup

# Start server  
make dev
```

### Method 4: Traditional
```bash
cd backend
pip install -r requirements.txt
python app.py
```

## 🔧 Available Commands

| Command | Python Script | Batch File | Makefile | Description |
|---------|---------------|------------|----------|-------------|
| **Development Server** | `python run.py dev` | `run.bat` | `make dev` | Start with auto-reload |
| **Production Server** | `python run.py prod` | `run.bat prod` | `make prod` | Start production server |
| **Install Dependencies** | `python run.py setup` | `run.bat setup` | `make setup` | Install requirements |
| **Run Tests** | `python run.py test` | `run.bat test` | `make test` | Run all tests |
| **Clean Cache** | `python run.py clean` | `run.bat clean` | `make clean` | Remove cache files |
| **Reset Data** | `python run.py reset` | `run.bat reset` | `make reset` | Reset models/uploads |

## 📋 Requirements

- **Python**: 3.8 or higher
- **pip**: For installing dependencies
- **Operating System**: Windows, macOS, or Linux

## 🌐 Access URLs

Once running, access these URLs:

- **Main Application**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs  
- **Health Check**: http://localhost:8000/health

## 🚨 Troubleshooting

### Issue: "Command not found"
**Solution**: Make sure you're in the ForgeML project directory.

### Issue: "Port 8000 is already in use"
**Solution**: 
1. Stop other services using port 8000
2. Or edit `backend/config.py` to change the port

### Issue: "Module not found"
**Solution**: 
```bash
python run.py setup   # Reinstall dependencies
```

### Issue: "Permission denied"
**Solution**:
- On Windows: Run as Administrator
- On macOS/Linux: Use `sudo` if needed

### Issue: Cache problems
**Solution**:
```bash
python run.py clean   # Clear cache files
```

## 🎯 Next Steps

1. **Upload a dataset** at http://localhost:8000
2. **Train your first model**
3. **Check out the API docs** at http://localhost:8000/docs
4. **Run tests** with `python run.py test`

## 📁 Project Structure

```
ForgeML/
├── 🚀 run.py           # Main runner script
├── 🪟 run.bat          # Windows batch runner  
├── 📄 Makefile         # Make commands
├── 📦 package.json     # NPM-style scripts
├── 🔧 .env.example     # Environment config template
├── 📚 backend/         # FastAPI backend
│   ├── app.py         # Main application
│   ├── config.py      # Configuration  
│   ├── requirements.txt
│   ├── api/           # API routes
│   ├── core/          # ML algorithms
│   ├── models/        # Saved models
│   ├── uploads/       # Uploaded datasets
│   └── templates/     # HTML templates
├── 📖 docs/           # Documentation
└── 🧪 test_*.py       # Test files
```

Happy coding! 🔥