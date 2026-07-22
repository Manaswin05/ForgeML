#!/usr/bin/env python3
"""
ForgeML - Easy Run Script
Usage: python run.py [command]

Commands:
  dev     - Start development server (default)
  prod    - Start production server
  test    - Run API tests
  setup   - Install dependencies
  clean   - Clean cache files
  reset   - Reset models and uploads
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

# Get project root
PROJECT_ROOT = Path(__file__).parent
BACKEND_DIR = PROJECT_ROOT / "backend"

def run_command(cmd, cwd=None):
    """Run a shell command with proper error handling."""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, check=True, 
                              capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        if e.stderr:
            print(f"Error output: {e.stderr}")
        return False

def install_dependencies():
    """Install Python dependencies."""
    print("📦 Installing dependencies...")
    return run_command("pip install -r requirements.txt", cwd=BACKEND_DIR)

def start_dev_server():
    """Start development server."""
    print("🚀 Starting ForgeML development server...")
    print("🌐 Server will be available at: http://localhost:8000")
    print("📖 API docs will be available at: http://localhost:8000/docs")
    print("Press Ctrl+C to stop the server\n")
    
    # Change to backend directory and run the app
    os.chdir(BACKEND_DIR)
    try:
        subprocess.run([sys.executable, "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

def start_prod_server():
    """Start production server."""
    print("🚀 Starting ForgeML production server...")
    return run_command("uvicorn app:app --host 0.0.0.0 --port 8000", cwd=BACKEND_DIR)

def run_tests():
    """Run API tests."""
    print("🧪 Running ForgeML tests...")
    success = True
    
    test_files = ["test_api.py", "test_weather_api.py", "test_predict.py"]
    for test_file in test_files:
        if (PROJECT_ROOT / test_file).exists():
            print(f"\n📋 Running {test_file}...")
            if not run_command(f"python {test_file}", cwd=PROJECT_ROOT):
                success = False
    
    return success

def clean_cache():
    """Clean Python cache files."""
    print("🧹 Cleaning cache files...")
    cache_dirs = [
        BACKEND_DIR / "__pycache__",
        BACKEND_DIR / "api" / "__pycache__",
        BACKEND_DIR / "core" / "__pycache__"
    ]
    
    for cache_dir in cache_dirs:
        if cache_dir.exists():
            import shutil
            shutil.rmtree(cache_dir)
            print(f"Removed {cache_dir}")

def reset_data():
    """Reset models and uploads directories."""
    print("🔄 Resetting data directories...")
    import shutil
    
    dirs_to_reset = [
        BACKEND_DIR / "models",
        BACKEND_DIR / "uploads"
    ]
    
    for dir_path in dirs_to_reset:
        if dir_path.exists():
            shutil.rmtree(dir_path)
        dir_path.mkdir(exist_ok=True)
        print(f"Reset {dir_path}")

def check_dependencies():
    """Check if dependencies are installed."""
    try:
        import fastapi
        import uvicorn
        return True
    except ImportError:
        return False

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="ForgeML Easy Run Script")
    parser.add_argument("command", nargs="?", default="dev", 
                       choices=["dev", "prod", "test", "setup", "clean", "reset"],
                       help="Command to run (default: dev)")
    
    args = parser.parse_args()
    
    print("🔥 ForgeML - ML Training Platform")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not BACKEND_DIR.exists():
        print("❌ Error: backend directory not found!")
        print("Make sure you're running this from the ForgeML project root.")
        sys.exit(1)
    
    # Handle commands
    if args.command == "setup":
        if install_dependencies():
            print("✅ Setup complete! Run 'python run.py dev' to start the server.")
        else:
            print("❌ Setup failed!")
            sys.exit(1)
    
    elif args.command == "dev":
        if not check_dependencies():
            print("❌ Dependencies not installed. Run 'python run.py setup' first.")
            sys.exit(1)
        start_dev_server()
    
    elif args.command == "prod":
        if not check_dependencies():
            print("❌ Dependencies not installed. Run 'python run.py setup' first.")
            sys.exit(1)
        start_prod_server()
    
    elif args.command == "test":
        if run_tests():
            print("✅ All tests passed!")
        else:
            print("❌ Some tests failed!")
            sys.exit(1)
    
    elif args.command == "clean":
        clean_cache()
        print("✅ Cache cleaned!")
    
    elif args.command == "reset":
        reset_data()
        print("✅ Data directories reset!")

if __name__ == "__main__":
    main()