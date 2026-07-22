#!/usr/bin/env python3
"""
Quick development launcher for ForgeML
Just run: python dev.py
"""

import os
import sys
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

# Import and run the main runner
from run import main

if __name__ == "__main__":
    # Force dev command
    sys.argv = [sys.argv[0], "dev"]
    main()