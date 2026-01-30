#!/bin/bash
# -*- coding: utf-8 -*-
# Skill Installation Script
#
# Usage:
#   chmod +x install.sh && ./install.sh
#

set -e

echo "🚀 Starting Skill Template installation..."
echo ""

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# Check Python version
echo "📋 Checking Python version..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
    echo "   ✅ Python version: $PYTHON_VERSION"
else
    echo "   ❌ Python3 not found"
    echo "   Please install Python 3.8+"
    exit 1
fi

# Check pip
echo ""
echo "📋 Checking pip..."
if command -v pip3 &> /dev/null; then
    echo "   ✅ pip available"
else
    echo "   ❌ pip not found"
    echo "   Installing pip..."
    python3 -m ensurepip --upgrade
fi

# Create venv (optional)
echo ""
read -p "Create virtual environment? (y/n): " CREATE_VENV
if [ "$CREATE_VENV" = "y" ] || [ "$CREATE_VENV" = "Y" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo "   ✅ Virtual environment created and activated"
fi

# Install dependencies
echo ""
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt
echo "   ✅ Dependencies installed"

# Check optional tools
echo ""
echo "📋 Checking optional tools..."

# Check ffmpeg
if command -v ffmpeg &> /dev/null; then
    echo "   ✅ ffmpeg installed"
else
    echo "   ⚠️ ffmpeg not found (optional)"
    echo "   To use video processing, run: brew install ffmpeg"
fi

# Create .env
echo ""
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "📄 Created .env from .env.example"
        echo "   Please edit .env to configure your API Key"
    fi
else
    echo "📄 .env already exists"
fi

# Create output directories
mkdir -p downloads cache
echo "📁 Created downloads and cache directories"

# Verify installation
echo ""
echo "🔍 Verifying installation..."
python3 cli.py status

echo ""
echo "════════════════════════════════════════════"
echo "✅ Installation complete!"
echo ""
echo "Usage:"
echo "  python3 cli.py status    # Check status"
echo "  python3 cli.py run xxx   # Execute task"
echo "  python3 cli.py --help    # Show help"
echo "════════════════════════════════════════════"
