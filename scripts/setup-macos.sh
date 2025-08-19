#!/bin/bash

# AP macOS Setup Script
# This script helps set up AP on macOS with all necessary dependencies

set -e

echo "🍎 AP macOS Setup Script"
echo "=========================="
echo ""

# Check if we're on macOS
if [[ "$(uname -s)" != "Darwin" ]]; then
    echo "❌ This script is for macOS only!"
    echo "   For Linux, please use the regular installation process."
    exit 1
fi

echo "✅ Detected macOS $(sw_vers -productVersion)"
echo ""

# Check for Xcode Command Line Tools
echo "🔧 Checking for Xcode Command Line Tools..."
if ! xcode-select -p &> /dev/null; then
    echo "📦 Installing Xcode Command Line Tools..."
    echo "   (This may take a few minutes and will open a dialog)"
    xcode-select --install
    echo "   Please complete the Xcode Command Line Tools installation"
    echo "   and run this script again."
    exit 0
else
    echo "✅ Xcode Command Line Tools are installed"
fi

# Check for Homebrew
echo ""
echo "🍺 Checking for Homebrew..."
if ! command -v brew &> /dev/null; then
    echo "📦 Installing Homebrew..."
    echo "   This will install Homebrew (the missing package manager for macOS)"
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    
    # Add Homebrew to PATH for Apple Silicon Macs
    if [[ "$(uname -m)" == "arm64" ]]; then
        echo "🔧 Adding Homebrew to PATH for Apple Silicon..."
        echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
        eval "$(/opt/homebrew/bin/brew shellenv)"
    fi
    
    echo "✅ Homebrew installed successfully!"
else
    echo "✅ Homebrew is already installed"
    echo "🔄 Updating Homebrew..."
    brew update
fi

# Check for Node.js
echo ""
echo "📦 Checking for Node.js..."
if ! command -v node &> /dev/null; then
    echo "📦 Installing Node.js via Homebrew..."
    brew install node
    echo "✅ Node.js installed successfully!"
else
    NODE_VERSION=$(node --version)
    echo "✅ Node.js is already installed ($NODE_VERSION)"
    
    # Check if version is >= 18
    NODE_MAJOR=$(echo $NODE_VERSION | cut -d'.' -f1 | sed 's/v//')
    if [[ $NODE_MAJOR -lt 18 ]]; then
        echo "⚠️  Node.js version is too old (need >= 18.0.0)"
        echo "📦 Updating Node.js..."
        brew upgrade node
    fi
fi

# Install optional but useful tools
echo ""
echo "🛠️  Installing useful optional tools..."

# Git (usually comes with Xcode tools, but let's make sure)
if ! command -v git &> /dev/null; then
    echo "📦 Installing Git..."
    brew install git
fi

# mas (Mac App Store CLI)
if ! command -v mas &> /dev/null; then
    echo "📦 Installing mas (Mac App Store CLI)..."
    brew install mas
    echo "✅ mas installed - you can now install App Store apps via CLI!"
else
    echo "✅ mas is already installed"
fi

# Check if user is signed into App Store
echo ""
echo "🏪 Checking Mac App Store sign-in status..."
if mas account &> /dev/null; then
    echo "✅ Signed into Mac App Store as: $(mas account)"
else
    echo "⚠️  Not signed into Mac App Store"
    echo "   To install App Store apps, please sign in:"
    echo "   System Preferences → Apple ID → Media & Purchases"
fi

echo ""
echo "🎉 macOS setup complete!"
echo ""
echo "📋 What's installed:"
echo "   ✅ Xcode Command Line Tools"
echo "   ✅ Homebrew ($(brew --version | head -1))"
echo "   ✅ Node.js ($(node --version))"
echo "   ✅ Git ($(git --version))"
echo "   ✅ mas (Mac App Store CLI)"
echo ""
echo "🚀 Next steps:"
echo "   1. Get your Gemini API key: https://aistudio.google.com/app/apikey"
echo "   2. Run: npm install && npm run build"
echo "   3. Run: ap init"
echo "   4. Start using AP!"
echo ""
echo "💡 Example commands to try:"
echo "   ap install visual studio code"
echo "   ap install firefox --cask"
echo "   ap install xcode --mas"
echo "   ap update system"