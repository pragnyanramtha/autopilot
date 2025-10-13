"""
Configuration Loader for Protocol System

Provides easy access to protocol system configuration settings from config.json.
"""

import json
import os
from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
class ValidationConfig:
    """Protocol validation configuration."""
    strict_mode: bool = False
    warning_level: str = "all"  # 'none', 'errors_only', 'all'


@dataclass
class VisualVerificationConfig:
    """Visual verification configuration."""
    enabled: bool = True
    timeout_seconds: int = 10
    confidence_threshold: float = 0.7
    primary_model: str = "gemini-flash-lite-latest"
    fallback_model: str = "gemini-2.5-flash"


@dataclass
class MouseMovementConfig:
    """Mouse movement configuration."""
    smooth: bool = True
    curve_type: str = "bezier"
    curve_intensity: float = 0.3
    speed: float = 1.0
    overshoot: bool = True
    overshoot_amount: float = 0.05
    add_noise: bool = True
    noise_amount: float = 2.0
    min_duration: float = 0.3
    max_duration: float = 1.5


@dataclass
class ActionLibraryConfig:
    """Action library configuration."""
    enabled_categories: List[str] = None
    disabled_actions: List[str] = None
    
    def __post_init__(self):
        if self.enabled_categories is None:
            self.enabled_categories = [
                "keyboard", "mouse", "window", "browser", "clipboard",
                "file", "screen", "timing", "vision", "system", "edit", "macro"
            ]
        if self.disabled_actions is None:
            self.disabled_actions = []
    
    def is_action_enabled(self, action_name: str, category: str) -> bool:
        """Check if an action is enabled."""
        if action_name in self.disabled_actions:
            return False
        if category not in self.enabled_categories:
            return False
        return True


@dataclass
class ProtocolConfig:
    """Complete protocol system configuration."""
    validation: ValidationConfig
    visual_verification: VisualVerificationConfig
    mouse_movement: MouseMovementConfig
    action_library: ActionLibraryConfig


class ConfigLoader:
    """
    Load and provide access to protocol system configuration.
    
    Usage:
        config = ConfigLoader.load()
        timeout = config.visual_verification.timeout_seconds
        strict = config.validation.strict_mode
    """
    
    _instance: Optional['ConfigLoader'] = None
    _config: Optional[ProtocolConfig] = None
    
    def __init__(self, config_path: str = "config.json"):
        """
        Initialize configuration loader.
        
        Args:
            config_path: Path to config.json file
        """
        self.config_path = config_path
        self._load_config()
    
    def _load_config(self) -> None:
        """Load configuration from config.json."""
        try:
            with open(self.config_path, 'r') as f:
                data = json.load(f)
            
            protocol_data = data.get('protocol', {})
            
            # Load validation config
            validation_data = protocol_data.get('validation', {})
            validation = ValidationConfig(
                strict_mode=validation_data.get('strict_mode', False),
                warning_level=validation_data.get('warning_level', 'all')
            )
            
            # Load visual verification config
            vision_data = protocol_data.get('visual_verification', {})
            visual_verification = VisualVerificationConfig(
                enabled=vision_data.get('enabled', True),
                timeout_seconds=vision_data.get('timeout_seconds', 10),
                confidence_threshold=vision_data.get('confidence_threshold', 0.7),
                primary_model=vision_data.get('primary_model', 'gemini-flash-lite-latest'),
                fallback_model=vision_data.get('fallback_model', 'gemini-2.5-flash')
            )
            
            # Load mouse movement config
            mouse_data = protocol_data.get('mouse_movement', {})
            mouse_movement = MouseMovementConfig(
                smooth=mouse_data.get('smooth', True),
                curve_type=mouse_data.get('curve_type', 'bezier'),
                curve_intensity=mouse_data.get('curve_intensity', 0.3),
                speed=mouse_data.get('speed', 1.0),
                overshoot=mouse_data.get('overshoot', True),
                overshoot_amount=mouse_data.get('overshoot_amount', 0.05),
                add_noise=mouse_data.get('add_noise', True),
                noise_amount=mouse_data.get('noise_amount', 2.0),
                min_duration=mouse_data.get('min_duration', 0.3),
                max_duration=mouse_data.get('max_duration', 1.5)
            )
            
            # Load action library config
            action_data = protocol_data.get('action_library', {})
            action_library = ActionLibraryConfig(
                enabled_categories=action_data.get('enabled_categories'),
                disabled_actions=action_data.get('disabled_actions', [])
            )
            
            self._config = ProtocolConfig(
                validation=validation,
                visual_verification=visual_verification,
                mouse_movement=mouse_movement,
                action_library=action_library
            )
            
        except FileNotFoundError:
            print(f"Warning: Config file not found at {self.config_path}, using defaults")
            self._config = self._get_default_config()
        except Exception as e:
            print(f"Warning: Error loading config: {e}, using defaults")
            self._config = self._get_default_config()
    
    def _get_default_config(self) -> ProtocolConfig:
        """Get default configuration."""
        return ProtocolConfig(
            validation=ValidationConfig(),
            visual_verification=VisualVerificationConfig(),
            mouse_movement=MouseMovementConfig(),
            action_library=ActionLibraryConfig()
        )
    
    @property
    def config(self) -> ProtocolConfig:
        """Get the loaded configuration."""
        return self._config
    
    @classmethod
    def load(cls, config_path: str = "config.json") -> ProtocolConfig:
        """
        Load configuration (singleton pattern).
        
        Args:
            config_path: Path to config.json file
            
        Returns:
            ProtocolConfig instance
        """
        if cls._instance is None:
            cls._instance = cls(config_path)
        return cls._instance.config
    
    @classmethod
    def reload(cls, config_path: str = "config.json") -> ProtocolConfig:
        """
        Force reload configuration from file.
        
        Args:
            config_path: Path to config.json file
            
        Returns:
            ProtocolConfig instance
        """
        cls._instance = cls(config_path)
        return cls._instance.config


# Convenience function for quick access
def get_config() -> ProtocolConfig:
    """
    Get protocol configuration.
    
    Returns:
        ProtocolConfig instance
        
    Example:
        from shared.config_loader import get_config
        
        config = get_config()
        timeout = config.visual_verification.timeout_seconds
    """
    return ConfigLoader.load()
