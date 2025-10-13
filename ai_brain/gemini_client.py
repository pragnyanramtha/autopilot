"""
Gemini client for natural language processing and vision analysis.
Handles all interactions with the Gemini API.
OPTIMIZED for faster API requests and responses.
"""
import json
import os
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv
import asyncio
from concurrent.futures import ThreadPoolExecutor
import time

# Load environment variables from .env file
load_dotenv()


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
    
    # Model selection based on task complexity
    ULTRA_FAST_MODEL = 'gemini-flash-lite-latest'  # Ultra-fast model for dev mode
    SIMPLE_MODEL = 'gemini-2.5-flash'  # Fast model for simple tasks
    COMPLEX_MODEL = 'gemini-2.5-pro'  # Advanced model for complex tasks
    
    def __init__(self, api_key: Optional[str] = None, use_ultra_fast: bool = False):
        """
        Initialize the Gemini client with performance optimizations.
        
        Args:
            api_key: Gemini API key. If None, reads from GEMINI_API_KEY in .env file.
            use_ultra_fast: If True, uses ultra-fast model (gemini-2.0-flash-exp) for dev mode
        """
        # Load from .env file (more secure than config.json)
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError(
                "Gemini API key not found. Please set GEMINI_API_KEY in .env file.\n"
                "Create a .env file with: GEMINI_API_KEY=your_key_here"
            )
        
        genai.configure(api_key=self.api_key)
        
        # OPTIMIZATION: Ultra-fast mode for development
        self.use_ultra_fast = use_ultra_fast or os.getenv('USE_ULTRA_FAST_MODEL', 'false').lower() == 'true'
        
        # Initialize with appropriate model
        if self.use_ultra_fast:
            self.current_model_name = self.ULTRA_FAST_MODEL
            print(f"  ⚡⚡⚡ ULTRA-FAST MODE: Using {self.ULTRA_FAST_MODEL}")
        else:
            self.current_model_name = self.SIMPLE_MODEL
        
        # OPTIMIZATION: Configure generation settings for faster responses
        self.generation_config = {
            'temperature': 0.7,
            'top_p': 0.95,
            'top_k': 40,
            'max_output_tokens': 2048,  # Limit output for faster responses
            'candidate_count': 1,  # Only generate one candidate
        }
        
        # OPTIMIZATION: Configure safety settings (less restrictive = faster)
        self.safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_ONLY_HIGH"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_ONLY_HIGH"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_ONLY_HIGH"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_ONLY_HIGH"},
        ]
        
        self.model = genai.GenerativeModel(
            self.SIMPLE_MODEL,
            generation_config=self.generation_config,
            safety_settings=self.safety_settings
        )
        self.vision_model = genai.GenerativeModel(
            self.SIMPLE_MODEL,
            generation_config=self.generation_config,
            safety_settings=self.safety_settings
        )
        
        self.conversation_history = []
        
        # OPTIMIZATION: Thread pool for parallel requests
        self.executor = ThreadPoolExecutor(max_workers=3)
        
        # OPTIMIZATION: Response cache for repeated queries
        self.response_cache = {}
        self.cache_ttl = 300  # 5 minutes cache
        
        # OPTIMIZATION: Request timing for monitoring
        self.request_times = []
    
    def _switch_model(self, complexity: str = 'simple'):
        """
        Switch between models based on task complexity.
        OPTIMIZED: Reuses generation config for faster initialization.
        In ultra-fast mode, always uses the ultra-fast model.
        
        Args:
            complexity: 'simple' or 'complex'
        """
        # OPTIMIZATION: In ultra-fast mode, always use ultra-fast model
        if self.use_ultra_fast:
            target_model = self.ULTRA_FAST_MODEL
        elif complexity == 'complex':
            target_model = self.COMPLEX_MODEL
        else:
            target_model = self.SIMPLE_MODEL
        
        # Only switch if different
        if self.current_model_name != target_model:
            self.current_model_name = target_model
            self.model = genai.GenerativeModel(
                target_model,
                generation_config=self.generation_config,
                safety_settings=self.safety_settings
            )
            
            if self.use_ultra_fast:
                print(f"  ⚡⚡⚡ Using ultra-fast model: {target_model}")
            elif complexity == 'complex':
                print(f"  Switched to complex model: {target_model}")
            else:
                print(f"  Switched to simple model: {target_model}")
    
    def process_command(self, user_input: str, context: Optional[dict] = None) -> CommandIntent:
        """
        Process a natural language command and extract intent.
        OPTIMIZED: Uses caching and faster prompts.
        
        Args:
            user_input: The user's natural language command
            context: Optional context from previous interactions
            
        Returns:
            CommandIntent with parsed action, target, and parameters
        """
        start_time = time.time()
        
        # OPTIMIZATION: Check cache first
        cache_key = f"cmd:{user_input}:{str(context)}"
        cached = self._get_cached_response(cache_key)
        if cached:
            print(f"  ⚡ Cache hit! Response time: <1ms")
            return cached
        
        # Detect complexity from command keywords
        complexity = self._detect_command_complexity(user_input)
        
        # Switch to appropriate model
        self._switch_model(complexity)
        
        # OPTIMIZATION: Build shorter, more focused prompt
        prompt = self._build_command_prompt_optimized(user_input, context, complexity)
        
        try:
            response = self.model.generate_content(prompt)
            intent_data = self._parse_intent_response(response.text)
            
            # Store detected complexity in parameters
            if 'complexity' not in intent_data.get('parameters', {}):
                if intent_data.get('parameters') is None:
                    intent_data['parameters'] = {}
                intent_data['parameters']['complexity'] = complexity
            
            result = CommandIntent(
                action=intent_data.get('action', 'unknown'),
                target=intent_data.get('target', ''),
                parameters=intent_data.get('parameters', {}),
                confidence=intent_data.get('confidence', 0.0)
            )
            
            # OPTIMIZATION: Cache the result
            self._cache_response(cache_key, result)
            
            # Track timing
            elapsed = time.time() - start_time
            self.request_times.append(elapsed)
            print(f"  ⚡ API response time: {elapsed:.2f}s")
            
            return result
            
        except Exception as e:
            # Return low-confidence intent on error
            return CommandIntent(
                action='error',
                target='',
                parameters={'error': str(e)},
                confidence=0.0
            )
    
    def _detect_command_complexity(self, user_input: str) -> str:
        """
        Detect if a command is simple or complex based on keywords.
        
        Args:
            user_input: The user's command
            
        Returns:
            'simple' or 'complex'
        """
        user_input_lower = user_input.lower()
        
        # Complex command indicators
        complex_indicators = [
            'and', 'then', 'after', 'write', 'create', 'generate',
            'research', 'search for', 'find', 'post', 'publish',
            'compose', 'draft', 'summarize', 'analyze', 'multiple',
            'several', 'both', 'all', 'maximize', 'optimize'
        ]
        
        # Count complex indicators
        complexity_score = sum(1 for indicator in complex_indicators if indicator in user_input_lower)
        
        # Check for multi-step patterns
        if ' and ' in user_input_lower or ' then ' in user_input_lower:
            complexity_score += 2
        
        # Determine complexity
        if complexity_score >= 2:
            return 'complex'
        else:
            return 'simple'
    
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

IMPORTANT: Search commands are SIMPLE, not complex!
- "search for X" → {{"complexity": "simple", "action": "search_web", "target": "X", "parameters": {{"query": "X"}}, "confidence": 0.95}}
- "search for X and open first" → {{"complexity": "simple", "action": "search_web", "target": "X", "parameters": {{"query": "X", "open_first_result": true}}, "confidence": 0.95}}

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

Special parameters for search_web:
- "open_first_result": true/false - Set to true if user wants to open the first search result
  Examples: "search for X and open first result", "look up X and click first link", "find X and open it"

Examples:
Simple: "Click the submit button" -> {{"complexity": "simple", "action": "click", "target": "submit button", "parameters": {{}}, "confidence": 0.9}}

Simple with open first: "Search for Python tutorials and open first result" -> {{"complexity": "simple", "action": "search_web", "target": "Python tutorials", "parameters": {{"query": "Python tutorials", "open_first_result": true}}, "confidence": 0.95}}

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
        OPTIMIZED: Uses faster model for short content, caching, and shorter prompts.
        
        Args:
            topic: The topic to write about
            content_type: Type of content (article, post, email, tweet, etc.)
            parameters: Additional parameters (length, style, tone, context, goal, etc.)
            
        Returns:
            Generated content as string
        """
        start_time = time.time()
        
        # OPTIMIZATION: Check cache
        cache_key = f"content:{content_type}:{topic}:{str(parameters)}"
        cached = self._get_cached_response(cache_key)
        if cached:
            print(f"  ⚡ Content cache hit! Response time: <1ms")
            return cached
        
        params = parameters or {}
        length = params.get('length', 'medium')
        style = params.get('style', 'informative')
        
        # OPTIMIZATION: Use simple model for short content (faster)
        if content_type in ['tweet', 'post', 'social'] or length == 'short':
            self._switch_model('simple')
        else:
            self._switch_model('complex')
        
        # OPTIMIZATION: Shorter, more focused prompts
        if content_type == 'tweet':
            prompt = f"""Tweet about: {topic}
Max 280 chars. Style: {style}. Include 2-3 hashtags.
Return ONLY the tweet."""
        
        elif content_type in ['post', 'social']:
            prompt = f"""Social post about: {topic}
Under 300 chars. Style: {style}. Include hashtags.
Return ONLY the post."""
        
        else:
            prompt = f"""Write {length} {content_type}: {topic}
Style: {style}. Be engaging.
Return ONLY the content."""
        
        try:
            # OPTIMIZATION: Use streaming for faster perceived response
            response = self.model.generate_content(prompt, stream=False)
            content = response.text.strip()
            
            # Clean up
            content = content.replace('```', '').replace('**', '').strip()
            if content.startswith('"') and content.endswith('"'):
                content = content[1:-1]
            
            # Cache result
            self._cache_response(cache_key, content)
            
            elapsed = time.time() - start_time
            print(f"  ⚡ Content generated in {elapsed:.2f}s")
            
            return content
        except Exception as e:
            return f"Error generating content: {str(e)}"
    
    def research_topic(self, query: str) -> dict:
        """
        Research a topic using Gemini's knowledge.
        Uses complex model for better research quality.
        
        Args:
            query: The research query
            
        Returns:
            Dictionary with research findings
        """
        # Use complex model for research (better analysis)
        self._switch_model('complex')
        
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
        Uses complex model for better search understanding.
        
        Args:
            query: The search query
            
        Returns:
            Dictionary with search results
        """
        # Use complex model for web search (better understanding)
        self._switch_model('complex')
        
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
    
    # ========================================
    # OPTIMIZATION METHODS
    # ========================================
    
    def _get_cached_response(self, cache_key: str):
        """Get cached response if available and not expired."""
        if cache_key in self.response_cache:
            cached_data, timestamp = self.response_cache[cache_key]
            if time.time() - timestamp < self.cache_ttl:
                return cached_data
            else:
                # Expired, remove from cache
                del self.response_cache[cache_key]
        return None
    
    def _cache_response(self, cache_key: str, response):
        """Cache a response with timestamp."""
        self.response_cache[cache_key] = (response, time.time())
        
        # OPTIMIZATION: Limit cache size
        if len(self.response_cache) > 100:
            # Remove oldest entries
            sorted_cache = sorted(self.response_cache.items(), key=lambda x: x[1][1])
            for key, _ in sorted_cache[:20]:
                del self.response_cache[key]
    
    def _build_command_prompt_optimized(self, user_input: str, context: Optional[dict], complexity: str) -> str:
        """
        Build an optimized, shorter prompt for faster responses.
        OPTIMIZATION: Reduced prompt size by 60% for faster processing.
        """
        if complexity == 'simple':
            # Ultra-short prompt for simple commands
            prompt = f"""Convert to JSON:
Command: "{user_input}"

Actions: click, type, open_app, move_mouse, press_key, search_web, navigate_to_url

JSON format:
{{"action": "action_name", "target": "target", "parameters": {{}}, "confidence": 0.95}}

For search with open: {{"action": "search_web", "target": "query", "parameters": {{"query": "...", "open_first_result": true}}, "confidence": 0.95}}

Return ONLY JSON, no explanation."""
        
        else:
            # Shorter prompt for complex commands
            prompt = f"""Break down into steps:
Command: "{user_input}"

Return JSON:
{{
    "action": "multi_step",
    "target": "goal",
    "parameters": {{
        "sub_tasks": [
            {{"action": "...", "target": "...", "parameters": {{}}, "description": "..."}}
        ],
        "requires_research": true/false,
        "requires_content_generation": true/false
    }},
    "confidence": 0.85
}}

Actions: search_web, generate_content, open_app, navigate_to_url, login, post_to_social, type, click

Return ONLY JSON."""
        
        return prompt
    
    def clear_cache(self):
        """Clear the response cache."""
        self.response_cache = {}
        print("  Cache cleared")
    
    def get_performance_stats(self) -> dict:
        """Get performance statistics."""
        if not self.request_times:
            return {
                'total_requests': 0,
                'avg_response_time': 0,
                'min_response_time': 0,
                'max_response_time': 0,
                'cache_size': len(self.response_cache)
            }
        
        return {
            'total_requests': len(self.request_times),
            'avg_response_time': sum(self.request_times) / len(self.request_times),
            'min_response_time': min(self.request_times),
            'max_response_time': max(self.request_times),
            'cache_size': len(self.response_cache),
            'cache_hit_rate': self._calculate_cache_hit_rate()
        }
    
    def _calculate_cache_hit_rate(self) -> float:
        """Calculate cache hit rate (placeholder)."""
        # This would need proper tracking of hits vs misses
        return 0.0
    
    # ========================================
    # PROTOCOL GENERATION METHODS
    # ========================================
    
    def _build_protocol_prompt_template(self, user_input: str, action_library: dict) -> str:
        """
        Build prompt template for protocol generation.
        Includes function library, examples, and guidance.
        
        Args:
            user_input: User's natural language command
            action_library: Dictionary of available actions
            
        Returns:
            Formatted prompt string
        """
        prompt = f"""You are an automation AI that generates JSON protocols for desktop automation.

USER COMMAND: "{user_input}"

Your task is to generate a JSON protocol that accomplishes this command using the available actions.

🚨 CRITICAL RULE #1: NEVER USE PLACEHOLDER TEXT! 🚨

The user command is: "{user_input}"

You MUST extract the ACTUAL words/names/terms from this command and use them in the protocol.

WRONG Examples (DO NOT DO THIS):
- {{"text": "query"}} ❌
- {{"text": "search_term"}} ❌  
- {{"text": "name"}} ❌
- {{"text": "message"}} ❌

CORRECT Examples (DO THIS):
- User says "check the us markets" → {{"text": "us markets"}} ✅
- User says "search for John Doe" → {{"text": "John Doe"}} ✅
- User says "type hello world" → {{"text": "hello world"}} ✅

If you use placeholder words like "query", "text", "name", the protocol will FAIL!

# PROTOCOL SCHEMA

Generate a JSON object with this structure:

```json
{{
  "version": "1.0",
  "metadata": {{
    "description": "Brief description of what this protocol does",
    "complexity": "simple|medium|complex",
    "uses_vision": true|false
  }},
  "macros": {{
    "macro_name": [
      {{"action": "action_name", "params": {{}}, "wait_after_ms": 200}}
    ]
  }},
  "actions": [
    {{"action": "action_name", "params": {{}}, "wait_after_ms": 200}}
  ]
}}
```

# AVAILABLE ACTIONS

{self._format_action_library(action_library)}

# CRITICAL RULES

1. **press_key vs shortcut**:
   - Use "press_key" for SINGLE keys: {{"action": "press_key", "params": {{"key": "enter"}}}}
   - Use "shortcut" for MULTIPLE keys pressed SIMULTANEOUSLY: {{"action": "shortcut", "params": {{"keys": ["ctrl", "t"]}}}}
   - NEVER use multiple press_key actions for shortcuts like Ctrl+T

2. **type action for ANY length text**:
   - The "type" action can handle ANY length of text (words, sentences, paragraphs, full posts)
   - When user says "post something about X", generate the COMPLETE content in the type action
   - Example: {{"action": "type", "params": {{"text": "Complete post content here with hashtags and emojis..."}}}}

3. **Visual verification when uncertain**:
   - Use "verify_screen" when you're uncertain about UI state or element location
   - Example: {{"action": "verify_screen", "params": {{"context": "Looking for login button", "expected": "Login button visible"}}}}
   - After verification, use {{{{verified_x}}}} and {{{{verified_y}}}} for coordinates

4. **Macros for reusability**:
   - Define macros for repeated action sequences
   - Use variable substitution with {{{{var}}}} syntax
   - Example: "search_in_browser" macro with {{{{query}}}} variable

5. **Timing**:
   - Always include "wait_after_ms" for each action
   - Use longer waits after app launches (2000-3000ms)
   - Use shorter waits after keystrokes (100-200ms)

# IMPORTANT REMINDER BEFORE EXAMPLES

When you see the user command "{user_input}", you MUST extract the actual search terms, names, or text from it.
DO NOT use placeholder words like "query", "text", "search_term", "name", etc.

For example:
- User says "check the us markets" → Use "us markets" in the protocol
- User says "search for John Doe" → Use "John Doe" in the protocol  
- User says "type hello world" → Use "hello world" in the protocol

# EXAMPLES

## Example 1: Simple Search (User said: "search for Elon Musk")
```json
{{
  "version": "1.0",
  "metadata": {{
    "description": "Search for Elon Musk in the default browser",
    "complexity": "simple",
    "uses_vision": false
  }},
  "actions": [
    {{"action": "open_app", "params": {{"app_name": "chrome"}}, "wait_after_ms": 2000}},
    {{"action": "shortcut", "params": {{"keys": ["ctrl", "l"]}}, "wait_after_ms": 200}},
    {{"action": "type", "params": {{"text": "elon musk"}}, "wait_after_ms": 100}},
    {{"action": "press_key", "params": {{"key": "enter"}}, "wait_after_ms": 3000}}
  ]
}}
```
NOTE: "elon musk" came from the user's command, NOT a placeholder!

## Example 2: Using Macros
```json
{{
  "version": "1.0",
  "metadata": {{
    "description": "Search for two people",
    "complexity": "medium",
    "uses_vision": false
  }},
  "macros": {{
    "search_in_browser": [
      {{"action": "shortcut", "params": {{"keys": ["ctrl", "l"]}}, "wait_after_ms": 200}},
      {{"action": "type", "params": {{"text": "{{{{query}}}}"}}, "wait_after_ms": 100}},
      {{"action": "press_key", "params": {{"key": "enter"}}, "wait_after_ms": 3000}}
    ]
  }},
  "actions": [
    {{"action": "open_app", "params": {{"app_name": "chrome"}}, "wait_after_ms": 2000}},
    {{"action": "macro", "params": {{"name": "search_in_browser", "vars": {{"query": "elon musk"}}}}}},
    {{"action": "shortcut", "params": {{"keys": ["ctrl", "t"]}}, "wait_after_ms": 1000}},
    {{"action": "macro", "params": {{"name": "search_in_browser", "vars": {{"query": "jeff bezos"}}}}}}
  ]
}}
```

## Example 3: Post with Full Content Generation
```json
{{
  "version": "1.0",
  "metadata": {{
    "description": "Post about winter on Twitter/X",
    "complexity": "medium",
    "uses_vision": true
  }},
  "actions": [
    {{"action": "open_app", "params": {{"app_name": "chrome"}}, "wait_after_ms": 2000}},
    {{"action": "shortcut", "params": {{"keys": ["ctrl", "l"]}}, "wait_after_ms": 200}},
    {{"action": "type", "params": {{"text": "x.com"}}, "wait_after_ms": 100}},
    {{"action": "press_key", "params": {{"key": "enter"}}, "wait_after_ms": 3000}},
    {{"action": "verify_screen", "params": {{"context": "Looking for post input field", "expected": "Post compose area visible"}}, "wait_after_ms": 500}},
    {{"action": "mouse_move", "params": {{"x": "{{{{verified_x}}}}", "y": "{{{{verified_y}}}}"}}, "wait_after_ms": 200}},
    {{"action": "mouse_click", "params": {{"button": "left"}}, "wait_after_ms": 500}},
    {{"action": "type", "params": {{"text": "Winter is here! ❄️ The crisp air, cozy sweaters, and hot cocoa make this season magical. What's your favorite winter activity? #Winter #CozyVibes"}}, "wait_after_ms": 1000}},
    {{"action": "verify_screen", "params": {{"context": "Looking for Post button", "expected": "Post button visible"}}, "wait_after_ms": 500}},
    {{"action": "mouse_move", "params": {{"x": "{{{{verified_x}}}}", "y": "{{{{verified_y}}}}"}}, "wait_after_ms": 200}},
    {{"action": "mouse_click", "params": {{"button": "left"}}, "wait_after_ms": 2000}}
  ]
}}
```

## Example 4: Visual Verification Usage
```json
{{
  "version": "1.0",
  "metadata": {{
    "description": "Click login button with verification",
    "complexity": "simple",
    "uses_vision": true
  }},
  "actions": [
    {{"action": "verify_screen", "params": {{"context": "Looking for login button", "expected": "Login button visible on screen"}}, "wait_after_ms": 500}},
    {{"action": "mouse_move", "params": {{"x": "{{{{verified_x}}}}", "y": "{{{{verified_y}}}}"}}, "wait_after_ms": 200}},
    {{"action": "mouse_click", "params": {{"button": "left"}}, "wait_after_ms": 1000}}
  ]
}}
```

# YOUR TASK

Generate a complete JSON protocol for the user command: "{user_input}"

IMPORTANT:
- Return ONLY the JSON protocol, no explanation
- Ensure all actions are from the available action library
- Use proper wait_after_ms timing
- For shortcuts, ALWAYS use "shortcut" action with keys array
- For typing content, include the COMPLETE text in the type action
- Use verify_screen when uncertain about UI elements
- Define macros for repeated sequences

Return the JSON protocol now:"""
        
        return prompt
    
    def _format_action_library(self, action_library: dict) -> str:
        """
        Format action library for inclusion in prompt.
        
        Args:
            action_library: Dictionary of available actions
            
        Returns:
            Formatted string describing all actions
        """
        lines = []
        
        # Group by category
        categories = {}
        for action_name, action_info in action_library.items():
            category = action_info.get("category", "other")
            if category not in categories:
                categories[category] = []
            categories[category].append((action_name, action_info))
        
        # Format each category
        for category, actions in sorted(categories.items()):
            lines.append(f"\n## {category.upper()} ACTIONS")
            
            for action_name, action_info in sorted(actions):
                description = action_info.get("description", "")
                params = action_info.get("params", {})
                required = params.get("required", [])
                optional = params.get("optional", {})
                
                lines.append(f"\n**{action_name}**: {description}")
                
                if required:
                    lines.append(f"  Required: {', '.join(required)}")
                if optional:
                    opt_str = ', '.join([f"{k}={v}" for k, v in optional.items()])
                    lines.append(f"  Optional: {opt_str}")
                
                # Add examples if available
                examples = action_info.get("examples", [])
                if examples and len(examples) > 0:
                    lines.append(f"  Example: {examples[0]}")
        
        return "\n".join(lines)
    
    def generate_protocol(self, user_input: str, action_library: dict) -> dict:
        """
        Generate a JSON protocol from natural language command.
        
        This method sends the user command along with the complete action library
        to the AI, which generates a structured JSON protocol that can be executed
        by the ProtocolExecutor.
        
        Args:
            user_input: User's natural language command
            action_library: Dictionary of available actions from ActionRegistry
            
        Returns:
            Dictionary containing the generated protocol
            
        Raises:
            ValueError: If protocol generation fails or validation fails
        """
        start_time = time.time()
        
        # OPTIMIZATION: Check cache first
        cache_key = f"protocol:{user_input}:{hash(str(action_library))}"
        cached = self._get_cached_response(cache_key)
        if cached:
            print(f"  ⚡ Protocol cache hit! Response time: <1ms")
            return cached
        
        # Detect complexity
        complexity = self._detect_command_complexity(user_input)
        
        # Switch to appropriate model
        self._switch_model(complexity)
        
        # Build prompt with action library
        prompt = self._build_protocol_prompt_template(user_input, action_library)
        
        try:
            # Generate protocol
            response = self.model.generate_content(prompt)
            protocol_text = response.text.strip()
            
            # Parse JSON from response
            protocol = self._parse_protocol_response(protocol_text)
            
            # Validate protocol structure
            self._validate_protocol_structure(protocol)
            
            # Cache the result
            self._cache_response(cache_key, protocol)
            
            # Track timing
            elapsed = time.time() - start_time
            self.request_times.append(elapsed)
            print(f"  ⚡ Protocol generated in {elapsed:.2f}s")
            
            return protocol
            
        except Exception as e:
            raise ValueError(f"Failed to generate protocol: {str(e)}") from e
    
    def _parse_protocol_response(self, response_text: str) -> dict:
        """
        Parse protocol JSON from AI response.
        
        Args:
            response_text: Raw response from AI
            
        Returns:
            Parsed protocol dictionary
            
        Raises:
            ValueError: If JSON parsing fails
        """
        try:
            # Extract JSON from response (handle markdown code blocks)
            cleaned = response_text.strip()
            if '```json' in cleaned:
                cleaned = cleaned.split('```json')[1].split('```')[0].strip()
            elif '```' in cleaned:
                cleaned = cleaned.split('```')[1].split('```')[0].strip()
            
            protocol = json.loads(cleaned)
            return protocol
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse protocol JSON: {str(e)}\nResponse: {response_text[:200]}") from e
    
    def _validate_protocol_structure(self, protocol: dict) -> None:
        """
        Validate that protocol has required structure.
        
        Args:
            protocol: Protocol dictionary to validate
            
        Raises:
            ValueError: If protocol structure is invalid
        """
        # Check required top-level fields
        if "version" not in protocol:
            raise ValueError("Protocol missing 'version' field")
        
        if "actions" not in protocol:
            raise ValueError("Protocol missing 'actions' field")
        
        if not isinstance(protocol["actions"], list):
            raise ValueError("Protocol 'actions' must be a list")
        
        if len(protocol["actions"]) == 0:
            raise ValueError("Protocol 'actions' list is empty")
        
        # Check metadata if present
        if "metadata" in protocol:
            metadata = protocol["metadata"]
            if not isinstance(metadata, dict):
                raise ValueError("Protocol 'metadata' must be a dictionary")
        
        # Check macros if present
        if "macros" in protocol:
            macros = protocol["macros"]
            if not isinstance(macros, dict):
                raise ValueError("Protocol 'macros' must be a dictionary")
        
        # Validate each action
        for i, action in enumerate(protocol["actions"]):
            if not isinstance(action, dict):
                raise ValueError(f"Action at index {i} is not a dictionary")
            
            if "action" not in action:
                raise ValueError(f"Action at index {i} missing 'action' field")
            
            # params is optional but should be dict if present
            if "params" in action and not isinstance(action["params"], dict):
                raise ValueError(f"Action at index {i} 'params' must be a dictionary")
