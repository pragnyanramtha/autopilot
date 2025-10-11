"""
Gemini client for natural language processing and vision analysis.
Handles all interactions with the Gemini API.
"""
import json
import os
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from PIL import Image
import google.generativeai as genai


@dataclass
class CommandIntent:
    """Represents the parsed intent from a user command."""
    action: str  # e.g., "click", "type", "open_app"
    target: str  # e.g., "Chrome icon", "search box"
    parameters: dict
    confidence: float


@dataclass
class ScreenAnalysis:
    """Represents the analysis of a screenshot."""
    elements: list[dict]  # Detected UI elements
    description: str
    suggested_coordinates: Optional[dict] = None


class GeminiClient:
    """Handles all interactions with Gemini API for NLP and vision."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Gemini client.
        
        Args:
            api_key: Gemini API key. If None, reads from GEMINI_API_KEY env var.
        """
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("Gemini API key not provided. Set GEMINI_API_KEY environment variable.")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        self.vision_model = genai.GenerativeModel('gemini-2.5-flash')
        self.conversation_history = []
    
    def process_command(self, user_input: str, context: Optional[dict] = None) -> CommandIntent:
        """
        Process a natural language command and extract intent.
        
        Args:
            user_input: The user's natural language command
            context: Optional context from previous interactions
            
        Returns:
            CommandIntent with parsed action, target, and parameters
        """
        # Build prompt for Gemini
        prompt = self._build_command_prompt(user_input, context)
        
        try:
            response = self.model.generate_content(prompt)
            intent_data = self._parse_intent_response(response.text)
            
            return CommandIntent(
                action=intent_data.get('action', 'unknown'),
                target=intent_data.get('target', ''),
                parameters=intent_data.get('parameters', {}),
                confidence=intent_data.get('confidence', 0.0)
            )
        except Exception as e:
            # Return low-confidence intent on error
            return CommandIntent(
                action='error',
                target='',
                parameters={'error': str(e)},
                confidence=0.0
            )
    
    def analyze_screen(self, screenshot: Image.Image) -> ScreenAnalysis:
        """
        Analyze a screenshot using Gemini's vision capabilities.
        
        Args:
            screenshot: PIL Image of the screen
            
        Returns:
            ScreenAnalysis with detected elements and coordinates
        """
        prompt = """Analyze this screenshot and identify all interactive UI elements.
        For each element, provide:
        1. Type (button, text_field, icon, menu, etc.)
        2. Label or description
        3. Approximate position (top-left, center, bottom-right, etc.)
        4. Estimated coordinates as percentage of screen (x%, y%)
        
        Return the analysis as JSON with this structure:
        {
            "description": "Overall description of the screen",
            "elements": [
                {
                    "type": "button",
                    "label": "Submit",
                    "position": "bottom-right",
                    "coordinates": {"x_percent": 85, "y_percent": 90}
                }
            ]
        }
        """
        
        try:
            response = self.vision_model.generate_content([prompt, screenshot])
            analysis_data = self._parse_screen_analysis(response.text)
            
            return ScreenAnalysis(
                elements=analysis_data.get('elements', []),
                description=analysis_data.get('description', ''),
                suggested_coordinates=analysis_data.get('suggested_coordinates')
            )
        except Exception as e:
            # Return empty analysis on error
            return ScreenAnalysis(
                elements=[],
                description=f"Error analyzing screen: {str(e)}",
                suggested_coordinates=None
            )
    
    def _build_command_prompt(self, user_input: str, context: Optional[dict]) -> str:
        """Build a prompt for command processing."""
        base_prompt = f"""You are an AI assistant that converts natural language commands into structured automation intents.

User command: "{user_input}"

Analyze this command and extract:
1. The primary action (click, type, open_app, move_mouse, search, etc.)
2. The target element or application
3. Any additional parameters (text to type, coordinates, etc.)
4. Your confidence level (0.0 to 1.0)

Return ONLY a JSON object with this structure:
{{
    "action": "the_action",
    "target": "the_target",
    "parameters": {{}},
    "confidence": 0.95
}}

Examples:
- "Click the submit button" -> {{"action": "click", "target": "submit button", "parameters": {{}}, "confidence": 0.9}}
- "Type hello world" -> {{"action": "type", "target": "", "parameters": {{"text": "hello world"}}, "confidence": 0.95}}
- "Open Chrome" -> {{"action": "open_app", "target": "Chrome", "parameters": {{}}, "confidence": 0.9}}
"""
        
        if context:
            base_prompt += f"\n\nContext from previous interaction: {json.dumps(context)}"
        
        return base_prompt
    
    def _parse_intent_response(self, response_text: str) -> dict:
        """Parse the Gemini response into intent data."""
        try:
            # Extract JSON from response (handle markdown code blocks)
            cleaned = response_text.strip()
            if '```json' in cleaned:
                cleaned = cleaned.split('```json')[1].split('```')[0].strip()
            elif '```' in cleaned:
                cleaned = cleaned.split('```')[1].split('```')[0].strip()
            
            return json.loads(cleaned)
        except json.JSONDecodeError:
            # Fallback parsing
            return {
                'action': 'unknown',
                'target': '',
                'parameters': {},
                'confidence': 0.0
            }
    
    def _parse_screen_analysis(self, response_text: str) -> dict:
        """Parse the Gemini vision response into screen analysis data."""
        try:
            # Extract JSON from response
            cleaned = response_text.strip()
            if '```json' in cleaned:
                cleaned = cleaned.split('```json')[1].split('```')[0].strip()
            elif '```' in cleaned:
                cleaned = cleaned.split('```')[1].split('```')[0].strip()
            
            return json.loads(cleaned)
        except json.JSONDecodeError:
            return {
                'description': response_text,
                'elements': []
            }
    
    def add_to_context(self, role: str, content: str):
        """Add a message to conversation history."""
        self.conversation_history.append({
            'role': role,
            'content': content,
            'timestamp': str(datetime.now())
        })
    
    def get_context(self) -> list[dict]:
        """Get conversation history."""
        return self.conversation_history
    
    def clear_context(self):
        """Clear conversation history."""
        self.conversation_history = []
