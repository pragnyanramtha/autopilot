#!/bin/bash

# Update Dependencies Script for Alvioli
echo "🔄 Updating Alvioli dependencies..."

# Remove node_modules and package-lock.json for clean install
echo "🧹 Cleaning old dependencies..."
rm -rf node_modules package-lock.json

# Install updated dependencies
echo "📦 Installing updated dependencies..."
npm install

# Check for any remaining vulnerabilities
echo "🔍 Checking for vulnerabilities..."
npm audit

# Run build to ensure everything works
echo "🔨 Testing build..."
npm run build

# Run linting
echo "🔍 Running linter..."
npm run lint

echo "✅ Dependency update complete!"
echo ""
echo "📋 Summary of major updates:"
echo "  • ESLint: v8 → v9 (new flat config)"
echo "  • Puppeteer: v21 → v23 (latest stable)"
echo "  • Chalk: v4 → v5 (ESM-only)"
echo "  • Commander: v11 → v12 (latest)"
echo "  • Inquirer: v8 → v12 (latest)"
echo "  • TypeScript: v5.2 → v5.6 (latest)"
echo "  • Node.js requirement: v16+ → v18+ (LTS)"
echo ""
echo "🚀 You can now run 'npm run dev' to test the application!"