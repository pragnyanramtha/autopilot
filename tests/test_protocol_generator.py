"""
Tests for ProtocolGenerator class.
"""
import pytest
from unittest.mock import Mock, MagicMock
from ai_brain.protocol_generator import ProtocolGenerator
from ai_brain.gemini_client import CommandIntent


def test_protocol_generator_initialization():
    """Test ProtocolGenerator initialization."""
    generator = ProtocolGenerator()
    assert generator.gemini_client is None
    assert generator.config == {}


def test_protocol_generator_with_config():
    """Test ProtocolGenerator with config."""
    config = {'test': 'value'}
    generator = ProtocolGenerator(config=config)
    assert generator.config == config


def test_create_protocol_requires_gemini_client():
    """Test that create_protocol requires a GeminiClient."""
    generator = ProtocolGenerator()
    intent = CommandIntent(action='test', target='test', parameters={}, confidence=1.0)
    
    with pytest.raises(ValueError, match="GeminiClient is required"):
        generator.create_protocol(intent)


def test_create_protocol_with_gemini_client():
    """Test create_protocol with a mocked GeminiClient."""
    # Mock GeminiClient
    mock_client = Mock()
    mock_protocol = {
        'version': '1.0',
        'metadata': {'id': 'test-123'},
        'actions': [
            {'action': 'open_app', 'params': {'app_name': 'chrome'}, 'wait_after_ms': 2000}
        ]
    }
    mock_client.generate_protocol.return_value = mock_protocol
    
    generator = ProtocolGenerator(gemini_client=mock_client)
    intent = CommandIntent(action='open_app', target='chrome', parameters={}, confidence=1.0)
    
    protocol = generator.create_protocol(intent, 'open chrome')
    
    assert protocol == mock_protocol
    mock_client.generate_protocol.assert_called_once_with('open chrome')


def test_validate_protocol_valid():
    """Test validate_protocol with valid protocol."""
    mock_client = Mock()
    generator = ProtocolGenerator(gemini_client=mock_client)
    
    valid_protocol = {
        'version': '1.0',
        'metadata': {'id': 'test-123'},
        'actions': [
            {'action': 'press_key', 'params': {'key': 'enter'}, 'wait_after_ms': 100}
        ]
    }
    
    result = generator.validate_protocol(valid_protocol)
    
    assert result['valid'] is True
    assert len(result['issues']) == 0


def test_validate_protocol_invalid():
    """Test validate_protocol with invalid protocol."""
    mock_client = Mock()
    generator = ProtocolGenerator(gemini_client=mock_client)
    
    invalid_protocol = {
        'version': '1.0',
        'actions': [
            {'action': 'invalid_action', 'params': {}, 'wait_after_ms': 100}
        ]
    }
    
    result = generator.validate_protocol(invalid_protocol)
    
    assert result['valid'] is False
    assert len(result['issues']) > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
