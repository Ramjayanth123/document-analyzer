#!/usr/bin/env python3
"""
Setup script for MCP Document Analyzer Server
Helps with initial environment setup and dependency installation.
"""

import os
import sys
import subprocess
import platform

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"Running: {description}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print(f"✗ Python {version.major}.{version.minor} is not supported. Please use Python 3.7+")
        return False
    print(f"✓ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def setup_virtual_environment():
    """Set up virtual environment."""
    if os.path.exists('venv'):
        print("✓ Virtual environment already exists")
        return True
    
    print("Creating virtual environment...")
    return run_command(f"{sys.executable} -m venv venv", "Virtual environment creation")

def install_dependencies():
    """Install required dependencies."""
    # Determine the correct pip path based on platform
    if platform.system() == "Windows":
        pip_path = "venv\\Scripts\\pip"
        python_path = "venv\\Scripts\\python"
    else:
        pip_path = "venv/bin/pip"
        python_path = "venv/bin/python"
    
    # Install dependencies
    if not run_command(f"{python_path} -m pip install --upgrade pip", "Pip upgrade"):
        return False
    
    if not run_command(f"{python_path} -m pip install -r requirements.txt", "Dependencies installation"):
        return False
    
    # Download required NLTK data
    print("Downloading NLTK data...")
    nltk_command = f"{python_path} -c \"import nltk; nltk.download('punkt', quiet=True); nltk.download('brown', quiet=True)\""
    return run_command(nltk_command, "NLTK data download")

def create_activation_script():
    """Create platform-specific activation script."""
    if platform.system() == "Windows":
        script_content = """@echo off
echo Activating MCP Document Analyzer environment...
call venv\\Scripts\\activate.bat
echo Environment activated! You can now run:
echo   python server.py    (to start the server)
echo   python test_client.py (to run tests)
echo   python -m deactivate (to deactivate environment)
"""
        with open("activate.bat", "w") as f:
            f.write(script_content)
        print("✓ Created activate.bat for Windows")
    else:
        script_content = """#!/bin/bash
echo "Activating MCP Document Analyzer environment..."
source venv/bin/activate
echo "Environment activated! You can now run:"
echo "  python server.py    (to start the server)"
echo "  python test_client.py (to run tests)"
echo "  deactivate (to deactivate environment)"
exec "$SHELL"
"""
        with open("activate.sh", "w") as f:
            f.write(script_content)
        os.chmod("activate.sh", 0o755)
        print("✓ Created activate.sh for Unix/Linux/macOS")

def main():
    """Main setup function."""
    print("MCP Document Analyzer Server - Setup Script")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Setup virtual environment
    if not setup_virtual_environment():
        print("Failed to set up virtual environment")
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("Failed to install dependencies")
        sys.exit(1)
    
    # Create activation script
    create_activation_script()
    
    print("\n" + "=" * 50)
    print("✓ Setup completed successfully!")
    print("=" * 50)
    print("\nNext steps:")
    if platform.system() == "Windows":
        print("1. Run: activate.bat")
        print("2. Run: python server.py")
        print("3. In another terminal, run: python test_client.py")
    else:
        print("1. Run: source activate.sh")
        print("2. Run: python server.py")
        print("3. In another terminal, run: python test_client.py")
    
    print("\nOr manually activate the environment:")
    if platform.system() == "Windows":
        print("  venv\\Scripts\\activate")
    else:
        print("  source venv/bin/activate")
    
    print("\nServer will be available at: http://localhost:8000")
    print("Documentation: README.md")

if __name__ == "__main__":
    main() 