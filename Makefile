# Alvioli Makefile for Node.js/TypeScript

# Build variables
APP_NAME=alvioli
DIST_DIR=dist
SRC_DIR=src

.PHONY: all build clean test deps install uninstall dev help

# Default target
all: clean deps build

# Install dependencies
deps:
	@echo "Installing dependencies..."
	@npm install

# Build TypeScript to JavaScript
build:
	@echo "Building $(APP_NAME)..."
	@npm run build
	@echo "Build complete: $(DIST_DIR)/"

# Build for development with watch
dev:
	@echo "Starting development mode..."
	@npm run dev

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	@npm run clean
	@echo "Clean complete"

# Run tests
test:
	@echo "Running tests..."
	@npm test

# Install globally using npm link
install: build
	@echo "Installing $(APP_NAME) globally..."
	@npm run install-global
	@echo "Installation complete"
	@echo "You can now use: alvioli, alido, or ali commands"

# Uninstall global installation
uninstall:
	@echo "Uninstalling $(APP_NAME)..."
	@npm unlink -g
	@echo "Uninstall complete"

# Run the application directly
run: build
	@echo "Running $(APP_NAME)..."
	@npm start

# Format code
fmt:
	@echo "Formatting code..."
	@npx prettier --write "$(SRC_DIR)/**/*.ts"

# Lint code
lint:
	@echo "Linting code..."
	@npm run lint

# Show help
help:
	@echo "Available targets:"
	@echo "  all        - Clean, install deps, and build"
	@echo "  build      - Build TypeScript to JavaScript"
	@echo "  dev        - Start development mode with ts-node"
	@echo "  clean      - Clean build artifacts"
	@echo "  test       - Run tests"
	@echo "  deps       - Install dependencies"
	@echo "  install    - Install globally (creates alvioli, alido, ali commands)"
	@echo "  uninstall  - Remove global installation"
	@echo "  run        - Build and run the application"
	@echo "  fmt        - Format code with prettier"
	@echo "  lint       - Lint code with eslint"
	@echo "  help       - Show this help message"