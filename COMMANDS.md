# 🚀 ForgeML Commands Reference

## 🎯 Quick Start Commands

### Fastest Way to Start
```bash
# One command to rule them all
python run.py setup

# Or just start if dependencies are installed
python run.py
```

### Windows Users
```bash
# Even easier with batch file
run.bat setup    # Install & setup
run.bat          # Start server
```

## 📋 All Available Commands

### 1. 🐍 Python Run Script (`run.py`)

| Command | Description | Example |
|---------|-------------|---------|
| `python run.py` | Start development server (default) | `python run.py` |
| `python run.py dev` | Start development server with auto-reload | `python run.py dev` |
| `python run.py prod` | Start production server | `python run.py prod` |
| `python run.py setup` | Install dependencies | `python run.py setup` |
| `python run.py test` | Run all tests | `python run.py test` |
| `python run.py clean` | Clean cache files | `python run.py clean` |
| `python run.py reset` | Reset models and uploads | `python run.py reset` |

### 2. 🪟 Windows Batch Files (`run.bat`)

| Command | Description |
|---------|-------------|
| `run.bat` | Start development server |
| `run.bat setup` | Install dependencies |
| `run.bat test` | Run tests |
| `run.bat clean` | Clean cache |
| `run.bat reset` | Reset data |

### 3. 🔧 Makefile Commands

| Command | Description |
|---------|-------------|
| `make` | Start development server |
| `make dev` | Start development server |
| `make setup` | Install dependencies |
| `make test` | Run tests |
| `make clean` | Clean cache |
| `make reset` | Reset data |
| `make help` | Show help |

### 4. 📦 NPM-Style Scripts (`package.json`)

| Command | Description |
|---------|-------------|
| `npm run dev` | Start development server |
| `npm run setup` | Install dependencies |
| `npm run test` | Run tests |
| `npm run cli` | Interactive CLI mode |
| `npm run browser` | Open in browser |
| `npm run status` | Check server status |

### 5. 🎮 Interactive CLI (`cli.py`)

#### Start Interactive Mode:
```bash
python cli.py                    # Interactive mode
python cli.py interactive        # Interactive mode (explicit)
```

#### Direct Commands:
| Command | Description | Example |
|---------|-------------|---------|
| `python cli.py server` | Start server | `python cli.py server` |
| `python cli.py status` | Check status | `python cli.py status` |
| `python cli.py upload <file>` | Upload dataset | `python cli.py upload data.csv` |
| `python cli.py models` | List saved models | `python cli.py models` |
| `python cli.py browser` | Open in browser | `python cli.py browser` |

#### Interactive Mode Commands:
Once in interactive mode (`python cli.py`):
```bash
🔥 ForgeML> server         # Start server
🔥 ForgeML> status         # Check status  
🔥 ForgeML> upload data.csv # Upload dataset
🔥 ForgeML> models         # List models
🔥 ForgeML> browser        # Open browser
🔥 ForgeML> help           # Show help
🔥 ForgeML> exit           # Exit
```

### 6. 🚀 Direct Launchers

| File | Description |
|------|-------------|
| `python dev.py` | Quick development launcher |
| `python backend/app.py` | Traditional method |

## 🎯 Common Workflows

### First Time Setup
```bash
# Method 1: All-in-one
python run.py setup

# Method 2: Step by step  
python run.py setup    # Install dependencies
python run.py dev      # Start server
```

### Daily Development
```bash
# Quick start (if deps installed)
python run.py          # or run.bat

# With auto-reload
python run.py dev

# Check what's running
python cli.py status
```

### Upload & Train Models
```bash
# Option 1: Use web interface
python run.py dev      # Start server
# Go to http://localhost:8000

# Option 2: Use CLI
python cli.py upload dataset.csv
python cli.py browser  # Open for training
```

### Testing & Debugging
```bash
python run.py test     # Run all tests
python run.py clean    # Clean cache if issues
python run.py reset    # Reset data if needed
```

### Production Deployment
```bash
python run.py prod     # Production server
```

## 🌐 Access URLs

Once server is running:

- **Main App**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Admin Interface**: http://localhost:8000/admin (if available)

## 🚨 Troubleshooting Commands

### Server Won't Start
```bash
python run.py clean    # Clean cache
python run.py setup    # Reinstall deps
python cli.py status   # Check status
```

### Port Issues
```bash
# Check what's using port 8000
netstat -ano | findstr :8000    # Windows
lsof -i :8000                   # macOS/Linux
```

### Reset Everything
```bash
python run.py clean    # Clean cache
python run.py reset    # Reset data
python run.py setup    # Reinstall
```

## 💡 Pro Tips

1. **Use aliases** for faster development:
   ```bash
   # Add to your shell profile:
   alias forge="python run.py"
   alias fdev="python run.py dev"
   alias fcli="python cli.py interactive"
   ```

2. **Bookmark URLs**:
   - Main: http://localhost:8000
   - Docs: http://localhost:8000/docs

3. **Use interactive CLI** for exploration:
   ```bash
   python cli.py
   ```

4. **Quick uploads**:
   ```bash
   python cli.py upload mydata.csv && python cli.py browser
   ```

Happy ForgeML development! 🔥