"""
Tests for Configuration Loader

Verifies that protocol system configuration is loaded correctly from config.json.
"""

import pytest
import json
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.config_loader import (
    ConfigLoader,
    get_config,
    ValidationConfig,
    VisualVerificationConfig,
    MouseMovementConfig,
    ActionLibraryConfig,
    ProtocolConfig
)


def test_load_config_from_file():
    """Test loading configuration from config.json."""
    config = ConfigLoader.load()
    
    assert config is not None
    assert isinstance(config, ProtocolConfig)
    assert isinstance(config.validation, ValidationConfig)
    assert isinstance(config.visual_verification, VisualVerificationConfig)
    assert isinstance(config.mouse_movement, MouseMovementConfig)
    assert isinstance(config.action_library, ActionLibraryConfig)


def test_validation_config():
    """Test validation configuration settings."""
    config = get_config()
    
    # Check validation settings
    assert isinstance(config.validation.strict_mode, bool)
    assert config.validation.warning_level in ['none', 'errors_only', 'all']


def test_visual_verification_config():
    """Test visual verification configuration settings."""
    config = get_config()
    
    # Check visual verification settings
    assert isinstance(config.visual_verification.enabled, bool)
    assert config.visual_verification.timeout_seconds > 0
    assert 0.0 <= config.visual_verification.confidence_threshold <= 1.0
    assert config.visual_verification.primary_model
    assert config.visual_verification.fallback_model


def test_mouse_movement_config():
    """Test mouse movement configuration settings."""
    config = get_config()
    
    # Check mouse movement settings
    assert isinstance(config.mouse_movement.smooth, bool)
    assert config.mouse_movement.curve_type in ['bezier', 'linear']
    assert 0.0 <= config.mouse_movement.curve_intensity <= 1.0
    assert config.mouse_movement.speed > 0
    assert isinstance(config.mouse_movement.overshoot, bool)
    assert 0.0 <= config.mouse_movement.overshoot_amount <= 1.0
    assert isinstance(config.mouse_movement.add_noise, bool)
    assert config.mouse_movement.noise_amount >= 0
    assert config.mouse_movement.min_duration > 0
    assert config.mouse_movement.max_duration > config.mouse_movement.min_duration


def test_action_library_config():
    """Test action library configuration settings."""
    config = get_config()
    
    # Check action library settings
    assert isinstance(config.action_library.enabled_categories, list)
    assert isinstance(config.action_library.disabled_actions, list)
    
    # Check default categories are present
    expected_categories = [
        "keyboard", "mouse", "window", "browser", "clipboard",
        "file", "screen", "timing", "vision", "system", "edit", "macro"
    ]
    for category in expected_categories:
        assert category in config.action_library.enabled_categories


def test_action_enabled_check():
    """Test checking if actions are enabled."""
    config = get_config()
    
    # Test enabled action
    assert config.action_library.is_action_enabled("press_key", "keyboard") == True
    
    # Test disabled category (if any)
    # This would fail if the category is not in enabled_categories
    
    # Test disabled action (if any in config)
    # This would fail if the action is in disabled_actions


def test_singleton_pattern():
    """Test that ConfigLoader uses singleton pattern."""
    config1 = ConfigLoader.load()
    config2 = ConfigLoader.load()
    
    # Should return the same instance
    assert config1 is config2


def test_get_config_convenience_function():
    """Test the convenience function for getting config."""
    config = get_config()
    
    assert config is not None
    assert isinstance(config, ProtocolConfig)


def test_config_values_match_file():
    """Test that loaded config values match config.json."""
    # Load config.json directly
    with open('config.json', 'r') as f:
        config_data = json.load(f)
    
    protocol_data = config_data.get('protocol', {})
    
    # Load via ConfigLoader
    config = get_config()
    
    # Compare validation settings
    validation_data = protocol_data.get('validation', {})
    assert config.validation.strict_mode == validation_data.get('strict_mode', False)
    assert config.validation.warning_level == validation_data.get('warning_level', 'all')
    
    # Compare visual verification settings
    vision_data = protocol_data.get('visual_verification', {})
    assert config.visual_verification.enabled == vision_data.get('enabled', True)
    assert config.visual_verification.timeout_seconds == vision_data.get('timeout_seconds', 10)
    assert config.visual_verification.confidence_threshold == vision_data.get('confidence_threshold', 0.7)
    
    # Compare mouse movement settings
    mouse_data = protocol_data.get('mouse_movement', {})
    assert config.mouse_movement.smooth == mouse_data.get('smooth', True)
    assert config.mouse_movement.curve_type == mouse_data.get('curve_type', 'bezier')
    assert config.mouse_movement.curve_intensity == mouse_data.get('curve_intensity', 0.3)


def test_default_config_on_missing_file():
    """Test that default config is used when file is missing."""
    # Create a loader with non-existent file
    loader = ConfigLoader(config_path="nonexistent.json")
    config = loader.config
    
    # Should still have valid config with defaults
    assert config is not None
    assert isinstance(config, ProtocolConfig)
    assert config.validation.strict_mode == False
    assert config.validation.warning_level == 'all'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
