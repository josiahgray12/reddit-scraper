#!/usr/bin/env python3
"""
Startup script for the Reddit scraper application.
This script handles virtual environment activation and application startup.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("Error: Python 3.8 or newer is required")
        sys.exit(1)

def is_venv_active():
    """Check if a virtual environment is currently active."""
    return hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)

def activate_venv():
    """Activate the virtual environment based on the operating system."""
    venv_path = Path("venv")
    if not venv_path.exists():
        print("Virtual environment not found. Creating one...")
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
    
    if platform.system() == "Windows":
        activate_script = venv_path / "Scripts" / "activate.bat"
        if not activate_script.exists():
            print(f"Error: Could not find activation script at {activate_script}")
            sys.exit(1)
        os.system(f"call {activate_script}")
    else:
        activate_script = venv_path / "bin" / "activate"
        if not activate_script.exists():
            print(f"Error: Could not find activation script at {activate_script}")
            sys.exit(1)
        os.system(f"source {activate_script}")

def install_requirements():
    """Install required packages if not already installed."""
    requirements_file = Path("requirements.txt")
    if not requirements_file.exists():
        print("Error: requirements.txt not found")
        sys.exit(1)
    
    print("Installing required packages...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)

def main():
    """Main entry point for the startup script."""
    print("Starting Reddit Scraper...")
    
    # Check Python version
    check_python_version()
    
    # Activate virtual environment if not already active
    if not is_venv_active():
        print("Virtual environment not active. Activating...")
        activate_venv()
        # Re-run the script with the activated environment
        os.execv(sys.executable, [sys.executable] + sys.argv)
    
    # Install requirements
    install_requirements()
    
    # Start the application
    print("\nStarting the application...")
    subprocess.run([sys.executable, "run.py"])

if __name__ == "__main__":
    main() 