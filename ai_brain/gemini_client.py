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
You excel at breaking down complex multi-step tasks into actionable workflows.

User command: "{user_input}"

Analyze this command and determine if it's:
1. SIMPLE: Single action (click, type, open app)
2. COMPLEX: Multiple sequential steps (research + write + post, login + navigate + submit)

For SIMPLE commands, return:
{{
    "complexity": "simple",
    "action": "the_action",
    "target": "the_target",
    "parameters": {{}},
    "confidence": 0.95
}}

For COMPLEX commands, break down into sub-tasks and return:
{{
    "complexity": "complex",
    "action": "multi_step",
    "target": "overall goal description",
    "parameters": {{
        "sub_tasks": [
            {{
                "action": "action1",
                "target": "target1",
                "parameters": {{}},
                "description": "what this step does"
            }},
            {{
                "action": "action2",
                "target": "target2",
                "parameters": {{}},
                "description": "what this step does"
            }}
        ],
        "requires_research": true/false,
        "requires_authentication": true/false,
        "requires_content_generation": true/false
    }},
    "confidence": 0.95
}}

Supported actions:
- Simple: click, type, open_app, move_mouse, press_key, double_click, right_click, wait
- Complex: search_web, navigate_to_url, login, fill_form, generate_content, post_to_social, send_email, multi_step

Examples:
Simple: "Click the submit button" -> {{"complexity": "simple", "action": "click", "target": "submit button", "parameters": {{}}, "confidence": 0.9}}

Complex: "Write an article about AI and post to X" -> 
{{
    "complexity": "complex",
    "action": "multi_step",
    "target": "write and post article about AI to X",
    "parameters": {{
        "sub_tasks": [
            {{"action": "search_web", "target": "AI latest trends", "parameters": {{"query": "latest AI trends 2025"}}, "description": "Research AI topics"}},
            {{"action": "generate_content", "target": "article", "parameters": {{"topic": "AI", "length": "medium", "style": "informative"}}, "description": "Write article about AI"}},
            {{"action": "open_app", "target": "Chrome", "parameters": {{}}, "description": "Open browser"}},
            {{"action": "navigate_to_url", "target": "https://x.com", "parameters": {{}}, "description": "Go to X"}},
            {{"action": "login", "target": "X", "parameters": {{"service": "x.com"}}, "description": "Login to X"}},
            {{"action": "post_to_social", "target": "X", "parameters": {{"platform": "x", "content_source": "generated"}}, "description": "Post the article"}}
        ],
        "requires_research": true,
        "requires_authentication": true,
        "requires_content_generation": true
    }},
    "confidence": 0.85
}}
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
    
    def generate_content(self, topic: str, content_type: str = "article", parameters: Optional[dict] = None) -> str:
        """
        Generate content using Gemini.
        
        Args:
            topic: The topic to write about
            content_type: Type of content (article, post, email, tweet, etc.)
            parameters: Additional parameters (length, style, tone, context, goal, etc.)
            
        Returns:
            Generated content as string
        """
        params = parameters or {}
        length = params.get('length', 'medium')
        style = params.get('style', 'informative')
        tone = params.get('tone', 'professional')
        context = params.get('context', '')
        goal = params.get('goal', '')
        
        # Special handling for tweets
        if content_type == 'tweet':
            prompt = f"""Create an engaging tweet about: {topic}

Requirements:
- Maximum 280 characters
- Style: {style}
- Goal: {goal if goal else 'maximize engagement'}
- Include relevant hashtags (2-3 max)
- Make it attention-grabbing
- Use questions, calls-to-action, or interesting facts
- Be concise and impactful

{f'Context: {context}' if context else ''}

Return ONLY the tweet text, no quotes or additional commentary."""
        
        elif content_type in ['post', 'social']:
            prompt = f"""Create an engaging social media post about: {topic}

Requirements:
- Keep it concise (under 300 characters)
- Style: {style}
- Goal: {goal if goal else 'maximize engagement'}
- Include relevant hashtags
- Make it shareable and engaging
- Use emojis if appropriate

{f'Context: {context}' if context else ''}

Return ONLY the post text, no additional commentary."""
        
        else:
            # Article or longer content
            length_guide = {
                'short': '1-2 paragraphs (100-200 words)',
                'medium': '3-5 paragraphs (300-500 words)',
                'long': '6-10 paragraphs (600-1000 words)'
            }
            
            prompt = f"""Write a {length} {content_type} about: {topic}

Requirements:
- Length: {length_guide.get(length, 'medium length')}
- Style: {style}
- Tone: {tone}
- Make it engaging and well-structured
- Include relevant examples or insights

{f'Context: {context}' if context else ''}
{f'Goal: {goal}' if goal else ''}

Return ONLY the content, no additional commentary."""
        
        try:
            response = self.model.generate_content(prompt)
            content = response.text.strip()
            
            # Clean up any markdown formatting or quotes
            content = content.replace('```', '').replace('**', '').strip()
            if content.startswith('"') and content.endswith('"'):
                content = content[1:-1]
            
            return content
        except Exception as e:
            return f"Error generating content: {str(e)}"
    
    def research_topic(self, query: str) -> dict:
        """
        Research a topic using Gemini's knowledge.
        
        Args:
            query: The research query
            
        Returns:
            Dictionary with research findings
        """
        prompt = f"""Research the following topic and provide key insights: {query}

Provide:
1. Main points and key facts
2. Current trends or developments
3. Important considerations
4. Relevant examples

Return as JSON:
{{
    "summary": "brief overview",
    "key_points": ["point1", "point2", "point3"],
    "trends": ["trend1", "trend2"],
    "examples": ["example1", "example2"]
}}"""
        
        try:
            response = self.model.generate_content(prompt)
            return self._parse_intent_response(response.text)
        except Exception as e:
            return {
                "summary": f"Error researching: {str(e)}",
                "key_points": [],
                "trends": [],
                "examples": []
            }
    
    def search_web_direct(self, query: str) -> dict:
        """
        Search the web directly using Gemini's grounding/search capabilities.
        This uses Gemini's built-in web search rather than browser automation.
        
        Args:
            query: The search query
            
        Returns:
            Dictionary with search results
        """
        prompt = f"""Search the web for: {query}

Provide the most relevant and current information you can find.
Include:
1. Top results summary
2. Key findings
3. Relevant links or sources (if available)
4. Current trends or news

Return as JSON:
{{
    "query": "{query}",
    "summary": "overview of findings",
    "results": [
        {{"title": "result title", "snippet": "brief description", "relevance": "high/medium/low"}},
        ...
    ],
    "key_findings": ["finding1", "finding2"],
    "trending_topics": ["topic1", "topic2"]
}}"""
        
        try:
            response = self.model.generate_content(prompt)
            result = self._parse_intent_response(response.text)
            result['query'] = query
            return result
        except Exception as e:
            return {
                "query": query,
                "summary": f"Error searching: {str(e)}",
                "results": [],
                "key_findings": [],
                "trending_topics": []
            }
    
    def get_user_input(self, prompt_text: str, default: str = "") -> str:
        """
        Request input from the user during workflow execution.
        This is a placeholder that would need to be integrated with the UI.
        
        Args:
            prompt_text: The prompt to show the user
            default: Default value if no input provided
            
        Returns:
            User's input as string
        """
        # This would need to be integrated with the main UI
        # For now, return a marker that the workflow generator can handle
        return f"[USER_INPUT_REQUIRED: {prompt_text}]"
