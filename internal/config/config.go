package config

import (
	"encoding/json"
	"os"
	"path/filepath"
)

// Config represents the application configuration
type Config struct {
	// Database settings
	DatabasePath string `json:"database_path"`
	
	// Browser settings
	BrowserPath     string `json:"browser_path,omitempty"`
	BrowserHeadless bool   `json:"browser_headless"`
	BrowserTimeout  int    `json:"browser_timeout"` // seconds
	
	// Terminal settings
	Shell           string `json:"shell"`
	CommandTimeout  int    `json:"command_timeout"` // seconds
	MaxRetries      int    `json:"max_retries"`
	
	// AI/Learning settings
	ContextRetention int     `json:"context_retention"` // days
	LearningEnabled  bool    `json:"learning_enabled"`
	SearchEnabled    bool    `json:"search_enabled"`
	
	// Security settings
	AllowRootCommands bool     `json:"allow_root_commands"`
	SafeMode          bool     `json:"safe_mode"`
	BlockedCommands   []string `json:"blocked_commands"`
	
	// Output settings
	Verbose     bool `json:"verbose"`
	ColorOutput bool `json:"color_output"`
	LogLevel    string `json:"log_level"`
}

// DefaultConfig returns the default configuration
func DefaultConfig() *Config {
	homeDir, _ := os.UserHomeDir()
	
	return &Config{
		DatabasePath:      filepath.Join(homeDir, ".alvioli", "alvioli.db"),
		BrowserHeadless:   false, // Visible browser as specified
		BrowserTimeout:    30,
		Shell:             "/bin/bash",
		CommandTimeout:    300, // 5 minutes
		MaxRetries:        3,
		ContextRetention:  30, // 30 days
		LearningEnabled:   true,
		SearchEnabled:     true,
		AllowRootCommands: true,
		SafeMode:          false,
		BlockedCommands:   []string{"rm -rf /", "mkfs", "dd if=/dev/zero"},
		Verbose:           false,
		ColorOutput:       true,
		LogLevel:          "info",
	}
}

// LoadConfig loads configuration from file or returns default
func LoadConfig(configPath string) (*Config, error) {
	if configPath == "" {
		homeDir, err := os.UserHomeDir()
		if err != nil {
			return DefaultConfig(), nil
		}
		configPath = filepath.Join(homeDir, ".alvioli", "config.json")
	}
	
	// If config file doesn't exist, return default config
	if _, err := os.Stat(configPath); os.IsNotExist(err) {
		return DefaultConfig(), nil
	}
	
	data, err := os.ReadFile(configPath)
	if err != nil {
		return DefaultConfig(), err
	}
	
	var config Config
	if err := json.Unmarshal(data, &config); err != nil {
		return DefaultConfig(), err
	}
	
	// Fill in any missing fields with defaults
	defaultConfig := DefaultConfig()
	if config.DatabasePath == "" {
		config.DatabasePath = defaultConfig.DatabasePath
	}
	if config.Shell == "" {
		config.Shell = defaultConfig.Shell
	}
	if config.CommandTimeout == 0 {
		config.CommandTimeout = defaultConfig.CommandTimeout
	}
	if config.MaxRetries == 0 {
		config.MaxRetries = defaultConfig.MaxRetries
	}
	
	return &config, nil
}

// SaveConfig saves configuration to file
func (c *Config) SaveConfig(configPath string) error {
	if configPath == "" {
		homeDir, err := os.UserHomeDir()
		if err != nil {
			return err
		}
		configPath = filepath.Join(homeDir, ".alvioli", "config.json")
	}
	
	// Create directory if it doesn't exist
	dir := filepath.Dir(configPath)
	if err := os.MkdirAll(dir, 0755); err != nil {
		return err
	}
	
	data, err := json.MarshalIndent(c, "", "  ")
	if err != nil {
		return err
	}
	
	return os.WriteFile(configPath, data, 0644)
}

// EnsureDirectories creates necessary directories for the application
func (c *Config) EnsureDirectories() error {
	dirs := []string{
		filepath.Dir(c.DatabasePath),
	}
	
	for _, dir := range dirs {
		if err := os.MkdirAll(dir, 0755); err != nil {
			return err
		}
	}
	
	return nil
}