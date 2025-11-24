#!/bin/bash
set -e

echo "🎨 Yadalist UI Design System - Quick Start"
echo "=========================================="
echo ""

# Check if node is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 20+ first."
    exit 1
fi

echo "✓ Node.js version: $(node --version)"
echo ""

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ Please run this script from the frontend/ directory"
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
npm install

echo ""
echo "🔨 Building CSS..."
npm run build

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Start development: npm run dev"
echo "  2. View Storybook: http://localhost:6006"
echo "  3. Check the README.md for usage examples"
echo ""
echo "Available commands:"
echo "  npm run dev          - Build CSS + run Storybook"
echo "  npm run build        - Build production CSS"
echo "  npm run watch:css    - Watch CSS changes only"
echo "  npm run storybook    - Run Storybook only"
echo ""
