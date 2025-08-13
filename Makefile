# Alvioli Makefile

# Build variables
BINARY_NAME=alvioli
BUILD_DIR=build
MAIN_PATH=cmd/main.go

# Go variables
GOCMD=go
GOBUILD=$(GOCMD) build
GOCLEAN=$(GOCMD) clean
GOTEST=$(GOCMD) test
GOGET=$(GOCMD) get
GOMOD=$(GOCMD) mod

# Build flags
LDFLAGS=-ldflags "-s -w"
BUILD_FLAGS=-trimpath

.PHONY: all build clean test deps install uninstall dev help

# Default target
all: clean deps build

# Build the binary
build:
	@echo "Building $(BINARY_NAME)..."
	@mkdir -p $(BUILD_DIR)
	$(GOBUILD) $(BUILD_FLAGS) $(LDFLAGS) -o $(BUILD_DIR)/$(BINARY_NAME) $(MAIN_PATH)
	@echo "Build complete: $(BUILD_DIR)/$(BINARY_NAME)"

# Build for development (with debug info)
dev:
	@echo "Building $(BINARY_NAME) for development..."
	@mkdir -p $(BUILD_DIR)
	$(GOBUILD) -o $(BUILD_DIR)/$(BINARY_NAME) $(MAIN_PATH)
	@echo "Development build complete: $(BUILD_DIR)/$(BINARY_NAME)"

# Clean build artifacts
clean:
	@echo "Cleaning build artifacts..."
	$(GOCLEAN)
	@rm -rf $(BUILD_DIR)
	@echo "Clean complete"

# Run tests
test:
	@echo "Running tests..."
	$(GOTEST) -v ./...

# Download dependencies
deps:
	@echo "Downloading dependencies..."
	$(GOMOD) download
	$(GOMOD) tidy

# Install binary to system
install: build
	@echo "Installing $(BINARY_NAME) to /usr/local/bin..."
	@sudo cp $(BUILD_DIR)/$(BINARY_NAME) /usr/local/bin/
	@sudo chmod +x /usr/local/bin/$(BINARY_NAME)
	@echo "Creating alido symlink..."
	@sudo ln -sf /usr/local/bin/$(BINARY_NAME) /usr/local/bin/alido
	@echo "Creating ali symlink..."
	@sudo ln -sf /usr/local/bin/$(BINARY_NAME) /usr/local/bin/ali
	@echo "Installation complete"

# Uninstall binary from system
uninstall:
	@echo "Uninstalling $(BINARY_NAME)..."
	@sudo rm -f /usr/local/bin/$(BINARY_NAME)
	@sudo rm -f /usr/local/bin/alido
	@sudo rm -f /usr/local/bin/ali
	@echo "Uninstall complete"

# Build for multiple platforms
build-all:
	@echo "Building for multiple platforms..."
	@mkdir -p $(BUILD_DIR)
	
	# Linux AMD64
	GOOS=linux GOARCH=amd64 $(GOBUILD) $(BUILD_FLAGS) $(LDFLAGS) -o $(BUILD_DIR)/$(BINARY_NAME)-linux-amd64 $(MAIN_PATH)
	
	# Linux ARM64
	GOOS=linux GOARCH=arm64 $(GOBUILD) $(BUILD_FLAGS) $(LDFLAGS) -o $(BUILD_DIR)/$(BINARY_NAME)-linux-arm64 $(MAIN_PATH)
	
	# Linux 386
	GOOS=linux GOARCH=386 $(GOBUILD) $(BUILD_FLAGS) $(LDFLAGS) -o $(BUILD_DIR)/$(BINARY_NAME)-linux-386 $(MAIN_PATH)
	
	@echo "Multi-platform build complete"

# Run the application
run: dev
	@echo "Running $(BINARY_NAME)..."
	@$(BUILD_DIR)/$(BINARY_NAME)

# Format code
fmt:
	@echo "Formatting code..."
	@$(GOCMD) fmt ./...

# Lint code (requires golangci-lint)
lint:
	@echo "Linting code..."
	@golangci-lint run

# Show help
help:
	@echo "Available targets:"
	@echo "  all        - Clean, download deps, and build"
	@echo "  build      - Build the binary"
	@echo "  dev        - Build for development (with debug info)"
	@echo "  clean      - Clean build artifacts"
	@echo "  test       - Run tests"
	@echo "  deps       - Download dependencies"
	@echo "  install    - Install binary to system (/usr/local/bin)"
	@echo "  uninstall  - Remove binary from system"
	@echo "  build-all  - Build for multiple platforms"
	@echo "  run        - Build and run the application"
	@echo "  fmt        - Format code"
	@echo "  lint       - Lint code (requires golangci-lint)"
	@echo "  help       - Show this help message"