"""
Protocol generator that converts CommandIntent into JSON protocols.
Replaces the old WorkflowGenerator with a protocol-based approach.
"""
import json
from typing import Optional
from ai_brain.gemini_client import CommandIntent, GeminiClient


class ProtocolGenerator:
    """Converts CommandIntent into JSON protocol for execution."""
    
    def __init__(self, gemini_client: Optional[GeminiClient] = None, config: Optional[dict] = None):
        """
        Initialize the protocol generator.
        
        Args:
            gemini_client: GeminiClient for protocol generation
            config: Optional configuration dictionary
        """
        self.gemini_client = gemini_client
        self.config = config or {}
    
    def create_protocol(self, intent: CommandIntent, user_input: str = "") -> dict:
        """
        Create a JSON protocol from a CommandIntent.
        
        Args:
            intent: The parsed command intent
            user_input: Original user input for context
            
        Returns:
            JSON protocol dictionary
        """
        if not self.gemini_client:
            raise ValueError("GeminiClient is required for protocol generation")
        
        # Use Gemini to generate the protocol
        protocol = self.gemini_client.generate_protocol(user_input or intent.target)
        
        return protocol
    
    def validate_protocol(self, protocol: dict) -> dict:
        """
        Validate a protocol for potential issues.
        
        Args:
            protocol: The protocol to validate
            
        Returns:
            Dictionary with validation results
        """
        from shared.protocol_parser import JSONProtocolParser
        
        parser = JSONProtocolParser()
        
        try:
            # Parse and validate
            parsed = parser.parse(protocol)
            
            return {
                'valid': True,
                'issues': [],
                'warnings': []
            }
        except Exception as e:
            return {
                'valid': False,
                'issues': [str(e)],
                'warnings': []
            }
