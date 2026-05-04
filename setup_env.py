#!/usr/bin/env python3
"""
Setup script for STIP (Structural Timeline of Intellectual Progression)
Install all dependencies and download required spaCy models.

Usage:
    python setup_env.py [--skip-models]
    
Options:
    --skip-models    Skip downloading spaCy models (faster, use if already installed)
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(command, description):
    """Run a shell command with progress output."""
    print(f"\n{'='*60}")
    print(f"📦 {description}")
    print(f"{'='*60}")
    print(f"Command: {' '.join(command)}\n")
    
    result = subprocess.run(command, capture_output=False)
    
    if result.returncode != 0:
        print(f"❌ Failed: {description}")
        return False
    
    print(f"✅ Success: {description}")
    return True


def check_python_version():
    """Check if Python version is compatible."""
    print("\n" + "="*60)
    print("🐍 Checking Python Version")
    print("="*60)
    
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required")
        return False
    
    print("✅ Python version is compatible")
    return True


def install_dependencies(skip_models=False):
    """Install all required dependencies."""
    # Upgrade pip first
    run_command(
        [sys.executable, "-m", "pip", "install", "--upgrade", "pip"],
        "Upgrading pip"
    )
    
    # Install requirements
    success = run_command(
        [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
        "Installing core dependencies from requirements.txt"
    )
    
    if not success:
        return False
    
    # Install optional development dependencies
    print("\n" + "="*60)
    print("🔧 Installing development tools")
    print("="*60)
    
    dev_deps = [
        "ipython>=8.0.0",
        "jupyter>=1.0.0",
        "pre-commit>=2.0.0"
    ]
    
    for dep in dev_deps:
        run_command(
            [sys.executable, "-m", "pip", "install", dep],
            f"Installing {dep}"
        )
    
    return True


def download_spacy_models():
    """Download required spaCy language models."""
    print("\n" + "="*60)
    print("🤖 Downloading spaCy Models")
    print("="*60)
    
    models = [
        ("en_core_web_sm", "Small English model (fast, recommended for testing)"),
        ("en_core_web_md", "Medium English model (balanced)"),
    ]
    
    for model, description in models:
        print(f"\n📥 Installing {model} - {description}")
        result = subprocess.run(
            [sys.executable, "-m", "spacy", "download", model],
            capture_output=False
        )
        
        if result.returncode == 0:
            print(f"✅ {model} installed successfully")
        else:
            print(f"⚠️  {model} installation failed (optional)")
    
    return True


def verify_installation():
    """Verify that all critical packages are installed correctly."""
    print("\n" + "="*60)
    print("✅ Verifying Installation")
    print("="*60)
    
    packages = [
        "spacy",
        "numpy",
        "pandas",
        "sklearn",
        "sentence_transformers",
        "matplotlib",
        "pytest",
    ]
    
    all_ok = True
    for package in packages:
        try:
            __import__(package)
            module = sys.modules[package]
            version = getattr(module, "__version__", "unknown")
            print(f"✅ {package:25} v{version}")
        except ImportError as e:
            print(f"❌ {package:25} NOT INSTALLED")
            all_ok = False
    
    # Check spaCy models
    try:
        import spacy
        try:
            nlp = spacy.load("en_core_web_sm")
            print(f"✅ en_core_web_sm          loaded successfully")
        except OSError:
            print(f"⚠️  en_core_web_sm          not found (run: python -m spacy download en_core_web_sm)")
    except:
        pass
    
    return all_ok


def create_virtual_env_guide():
    """Create a guide for virtual environment setup."""
    guide = """# Virtual Environment Setup Guide

## Recommended: Using venv

```bash
# Create virtual environment
python -m venv venv

# Activate on Linux/Mac
source venv/bin/activate

# Activate on Windows
venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt

# Run setup script
python setup_env.py
```

## Alternative: Using conda

```bash
# Create conda environment
conda create -n stip python=3.9

# Activate environment
conda activate stip

# Install dependencies
pip install -r requirements.txt

# Run setup script
python setup_env.py
```

## Quick Start

After activation, simply run:
```bash
pip install -r requirements.txt
python setup_env.py
```

Then test the installation:
```bash
pytest tests/
python examples/analyze_attention.py
```
"""
    
    guide_path = Path("VIRTUAL_ENV_GUIDE.md")
    guide_path.write_text(guide)
    print(f"\n📝 Created {guide_path}")


def main():
    """Main setup function."""
    print("\n" + "="*60)
    print("🚀 STIP Development Environment Setup")
    print("="*60)
    print("\nThis script will set up your local development environment.")
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Parse arguments
    skip_models = "--skip-models" in sys.argv
    
    # Install dependencies
    if not install_dependencies(skip_models):
        print("\n❌ Dependency installation failed")
        sys.exit(1)
    
    # Download spaCy models (unless skipped)
    if not skip_models:
        download_spacy_models()
    
    # Verify installation
    all_ok = verify_installation()
    
    # Create virtual env guide
    create_virtual_env_guide()
    
    # Final summary
    print("\n" + "="*60)
    print("🎉 Setup Complete!")
    print("="*60)
    
    if all_ok:
        print("\n✅ All critical packages installed successfully")
        print("\nNext steps:")
        print("  1. Run tests: pytest tests/")
        print("  2. Try example: python examples/analyze_attention.py")
        print("  3. Start developing! 🚀")
    else:
        print("\n⚠️  Some packages may need manual installation")
        print("   Check the errors above and try: pip install <package-name>")
    
    print("\n📚 See VIRTUAL_ENV_GUIDE.md for more details")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
