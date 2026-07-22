#!/usr/bin/env python3
"""
ForgeML CLI - Command Line Interface
Advanced CLI with interactive features
"""

import os
import sys
import subprocess
import argparse
import json
from pathlib import Path
import requests
import time

# Get project root
PROJECT_ROOT = Path(__file__).parent
BACKEND_DIR = PROJECT_ROOT / "backend"

class ForgeMLCLI:
    def __init__(self):
        self.base_url = "http://localhost:8000"
        
    def print_header(self):
        """Print ForgeML header."""
        print("""
🔥 ForgeML CLI - Command Line Interface
========================================
        """)
    
    def check_server_running(self):
        """Check if the ForgeML server is running."""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def start_server(self, background=False):
        """Start the ForgeML server."""
        if self.check_server_running():
            print("✅ Server is already running at http://localhost:8000")
            return True
            
        print("🚀 Starting ForgeML server...")
        
        if background:
            # Start server in background
            cmd = [sys.executable, "app.py"]
            subprocess.Popen(cmd, cwd=BACKEND_DIR)
            
            # Wait for server to start
            for i in range(30):  # Wait up to 30 seconds
                if self.check_server_running():
                    print("✅ Server started successfully!")
                    return True
                time.sleep(1)
                print(f"⏳ Waiting for server... ({i+1}/30)")
            
            print("❌ Server failed to start")
            return False
        else:
            # Start server in foreground
            try:
                cmd = [sys.executable, "app.py"]
                subprocess.run(cmd, cwd=BACKEND_DIR)
                return True
            except KeyboardInterrupt:
                print("\n👋 Server stopped")
                return True
            except Exception as e:
                print(f"❌ Error starting server: {e}")
                return False
    
    def upload_dataset(self, file_path):
        """Upload a dataset via API."""
        if not self.check_server_running():
            print("❌ Server is not running. Start it with: python cli.py server")
            return False
            
        file_path = Path(file_path)
        if not file_path.exists():
            print(f"❌ File not found: {file_path}")
            return False
            
        print(f"📤 Uploading {file_path.name}...")
        
        try:
            with open(file_path, 'rb') as f:
                files = {'file': f}
                response = requests.post(f"{self.base_url}/api/upload", files=files)
                
            if response.status_code == 200:
                data = response.json()
                info = data['info']
                print(f"✅ Dataset uploaded successfully!")
                print(f"   📊 {info['rows']} rows, {info['columns']} columns")
                print(f"   📋 Columns: {', '.join(info['column_names'][:5])}{'...' if len(info['column_names']) > 5 else ''}")
                return True
            else:
                print(f"❌ Upload failed: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error uploading: {e}")
            return False
    
    def get_status(self):
        """Get current session status."""
        if not self.check_server_running():
            print("❌ Server is not running")
            return False
            
        try:
            response = requests.get(f"{self.base_url}/api/status")
            if response.status_code == 200:
                data = response.json()
                print("📊 Current Session Status:")
                print(f"   🔄 Status: {data['status']}")
                print(f"   📈 Has Data: {'Yes' if data['has_data'] else 'No'}")
                print(f"   🤖 Has Model: {'Yes' if data['has_model'] else 'No'}")
                if data['has_data']:
                    print(f"   📋 Data Rows: {data['data_rows']}")
                if data['model_type']:
                    print(f"   🎯 Model Type: {data['model_type']}")
                if data['task_type']:
                    print(f"   📊 Task Type: {data['task_type']}")
                return True
            else:
                print(f"❌ Failed to get status: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Error getting status: {e}")
            return False
    
    def list_models(self):
        """List available saved models."""
        models_dir = BACKEND_DIR / "models"
        model_files = list(models_dir.glob("*.pkl"))
        
        if not model_files:
            print("📦 No saved models found")
            return
            
        print(f"📦 Found {len(model_files)} saved models:")
        for model_file in model_files:
            # Try to load metadata
            metadata_file = model_file.with_suffix('.pkl.metadata.json')
            if metadata_file.exists():
                try:
                    with open(metadata_file) as f:
                        metadata = json.load(f)
                    print(f"   🤖 {model_file.name}")
                    print(f"      📊 Type: {metadata.get('model_type', 'Unknown')}")
                    print(f"      🎯 Task: {metadata.get('task_type', 'Unknown')}")
                    print(f"      📈 Format: {metadata.get('export_format', 'pickle')}")
                    print(f"      🗜️ Compressed: {metadata.get('compressed', 'Unknown')}")
                except:
                    print(f"   🤖 {model_file.name} (no metadata)")
            else:
                print(f"   🤖 {model_file.name} (no metadata)")
    
    def open_browser(self):
        """Open ForgeML in browser."""
        if not self.check_server_running():
            print("❌ Server is not running. Starting server first...")
            if not self.start_server(background=True):
                return False
                
        print("🌐 Opening ForgeML in your browser...")
        import webbrowser
        webbrowser.open("http://localhost:8000")
        return True
    
    def interactive_mode(self):
        """Run interactive CLI mode."""
        self.print_header()
        print("🎮 Interactive Mode - Type 'help' for commands, 'exit' to quit")
        
        while True:
            try:
                command = input("\n🔥 ForgeML> ").strip().lower()
                
                if command in ['exit', 'quit', 'q']:
                    print("👋 Goodbye!")
                    break
                elif command in ['help', 'h', '?']:
                    self.show_interactive_help()
                elif command in ['status', 'st']:
                    self.get_status()
                elif command in ['server', 'start']:
                    self.start_server()
                elif command in ['models', 'ls']:
                    self.list_models()
                elif command in ['browser', 'web', 'open']:
                    self.open_browser()
                elif command.startswith('upload '):
                    file_path = command.split(' ', 1)[1]
                    self.upload_dataset(file_path)
                elif command == '':
                    continue
                else:
                    print(f"❓ Unknown command: {command}")
                    print("   Type 'help' for available commands")
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except EOFError:
                print("\n👋 Goodbye!")
                break
    
    def show_interactive_help(self):
        """Show interactive mode help."""
        print("""
📚 Available Commands:
  
  🚀 Server Management:
    server, start     - Start the ForgeML server
    status, st        - Show current session status
    
  📊 Data Management:
    upload <file>     - Upload a dataset file
    models, ls        - List saved models
    
  🌐 Interface:
    browser, web      - Open ForgeML in browser
    
  ❓ Help & Exit:
    help, h, ?        - Show this help
    exit, quit, q     - Exit interactive mode
    
  💡 Examples:
    upload data.csv   - Upload data.csv file
    server            - Start the server
    browser           - Open in browser
        """)

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="ForgeML CLI - Advanced Command Line Interface")
    parser.add_argument('command', nargs='?', 
                       choices=['server', 'upload', 'status', 'models', 'browser', 'interactive'],
                       help='Command to run')
    parser.add_argument('file', nargs='?', help='File path for upload command')
    parser.add_argument('--background', '-b', action='store_true', 
                       help='Start server in background')
    
    args = parser.parse_args()
    
    cli = ForgeMLCLI()
    
    if not args.command:
        # No command provided, run interactive mode
        cli.interactive_mode()
        return
    
    cli.print_header()
    
    if args.command == 'server':
        cli.start_server(background=args.background)
    elif args.command == 'upload':
        if not args.file:
            print("❌ Please provide a file path: python cli.py upload <file>")
            sys.exit(1)
        cli.upload_dataset(args.file)
    elif args.command == 'status':
        cli.get_status()
    elif args.command == 'models':
        cli.list_models()
    elif args.command == 'browser':
        cli.open_browser()
    elif args.command == 'interactive':
        cli.interactive_mode()

if __name__ == "__main__":
    main()