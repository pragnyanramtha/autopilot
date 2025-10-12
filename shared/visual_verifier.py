"""
Visual Verification System for JSON Instruction Protocol

This module provides visual verification capabilities using Gemini vision models.
It allows the protocol executor to pause execution, capture screenshots, and
verify screen state using AI vision analysis.

Requirements:
- 11.1: Pause workflow execution for verification
- 11.2: Capture screenshot and send to Gemini
- 11.3: Receive AI analysis and resume/adapt
- 11.4: Multi-model support with fallback
- 13.1-13.4: Model configuration and error handling
"""

import time
import base64
import io
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass
from PIL import Image
import google.generativeai as genai


@dataclass
class VerificationResult:
    """Result from visual verification."""
    safe_to_proceed: bool
    confidence: float
    analysis: str
    updated_coordinates: Optional[Dict[str, int]] = None
    suggested_actions: Optional[list] = None
    model_used: str = "unknown"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'safe_to_proceed': self.safe_to_proceed,
            'confidence': self.confidence,
            'analysis': self.analysis,
            'updated_coordinates': self.updated_coordinates,
            'suggested_actions': self.suggested_actions,
            'model_used': self.model_used
        }


class VisualVerifier:
    """
    Visual verification system using Gemini vision models.
    
    Supports:
    - Screenshot capture and analysis
    - Multi-model support (primary + fallback)
    - Coordinate extraction from AI responses
    - Adaptive execution based on verification results
    
    Requirements:
    - 11.1: Pause and verify screen state
    - 11.2: Screenshot capture and AI analysis
    - 11.3: Parse AI response and extract coordinates
    - 11.4: Multi-model support with automatic fallback
    - 13.1-13.4: Configuration and error handling
    """
    
    # Model configuration
    PRIMARY_MODEL = 'gemini-2.0-flash-exp'  # Gemini 2.5 Flash Live API equivalent
    FALLBACK_MODEL = 'gemini-1.5-flash'  # gemini-flash-lite-latest equivalent
    
    def __init__(
        self,
        screen_capture,
        api_key: str,
        primary_model: Optional[str] = None,
        fallback_model: Optional[str] = None,
        timeout_seconds: int = 10
    ):
        """
        Initialize the visual verifier.
        
        Args:
            screen_capture: ScreenCapture instance for capturing screenshots
            api_key: Gemini API key
            primary_model: Primary vision model name (default: gemini-2.0-flash-exp)
            fallback_model: Fallback model name (default: gemini-1.5-flash)
            timeout_seconds: Timeout for API requests (default: 10s)
            
        Requirements:
        - 13.1: Configure primary model
        - 13.2: Configure fallback model
        - 13.3: Timeout configuration
        """
        self.screen_capture = screen_capture
        self.api_key = api_key
        self.primary_model_name = primary_model or self.PRIMARY_MODEL
        self.fallback_model_name = fallback_model or self.FALLBACK_MODEL
        self.timeout_seconds = timeout_seconds
        
        # Configure Gemini API
        genai.configure(api_key=api_key)
        
        # Initialize models
        self._init_models()
        
        # Statistics
        self.verification_count = 0
        self.fallback_count = 0
        self.error_count = 0
    
    def _init_models(self):
        """Initialize vision models with configuration."""
        # Generation config optimized for vision tasks
        self.generation_config = {
            'temperature': 0.3,  # Lower temperature for more consistent analysis
            'top_p': 0.95,
            'top_k': 40,
            'max_output_tokens': 1024,
        }
        
        # Safety settings
        self.safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_ONLY_HIGH"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_ONLY_HIGH"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_ONLY_HIGH"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_ONLY_HIGH"},
        ]
        
        try:
            # Initialize primary model
            self.primary_model = genai.GenerativeModel(
                self.primary_model_name,
                generation_config=self.generation_config,
                safety_settings=self.safety_settings
            )
            print(f"✓ Primary vision model initialized: {self.primary_model_name}")
        except Exception as e:
            print(f"⚠ Warning: Could not initialize primary model: {e}")
            self.primary_model = None
        
        try:
            # Initialize fallback model
            self.fallback_model = genai.GenerativeModel(
                self.fallback_model_name,
                generation_config=self.generation_config,
                safety_settings=self.safety_settings
            )
            print(f"✓ Fallback vision model initialized: {self.fallback_model_name}")
        except Exception as e:
            print(f"⚠ Warning: Could not initialize fallback model: {e}")
            self.fallback_model = None
        
        if not self.primary_model and not self.fallback_model:
            raise RuntimeError("Failed to initialize any vision models")
    
    def verify_screen(
        self,
        context: str,
        expected: str,
        confidence_threshold: float = 0.7,
        capture_region: Optional[Tuple[int, int, int, int]] = None
    ) -> VerificationResult:
        """
        Verify screen state using AI vision analysis.
        
        This is the main entry point for visual verification. It:
        1. Captures a screenshot
        2. Sends it to Gemini vision model
        3. Parses the AI response
        4. Extracts coordinates if provided
        5. Returns verification result
        
        Args:
            context: Context about what we're verifying (e.g., "Looking for login button")
            expected: What we expect to see (e.g., "Login button visible and clickable")
            confidence_threshold: Minimum confidence to proceed (0.0-1.0)
            capture_region: Optional (x, y, width, height) to capture specific region
            
        Returns:
            VerificationResult with analysis and coordinates
            
        Requirements:
        - 11.1: Pause execution and verify
        - 11.2: Capture and analyze screenshot
        - 11.3: Parse response and extract coordinates
        - 11.4: Automatic fallback on failure
        """
        self.verification_count += 1
        
        print(f"\n🔍 Visual Verification #{self.verification_count}")
        print(f"  Context: {context}")
        print(f"  Expected: {expected}")
        
        # Capture screenshot
        try:
            if capture_region:
                x, y, width, height = capture_region
                screenshot = self.screen_capture.capture_region(x, y, width, height)
                print(f"  Captured region: {width}x{height} at ({x}, {y})")
            else:
                screenshot = self.screen_capture.capture_screen()
                print(f"  Captured full screen")
        except Exception as e:
            self.error_count += 1
            return VerificationResult(
                safe_to_proceed=False,
                confidence=0.0,
                analysis=f"Failed to capture screenshot: {str(e)}",
                model_used="none"
            )
        
        # Try primary model first
        result = self._verify_with_model(
            screenshot,
            context,
            expected,
            confidence_threshold,
            use_primary=True
        )
        
        # If primary failed, try fallback
        if result is None and self.fallback_model:
            print(f"  ⚠ Primary model failed, trying fallback...")
            self.fallback_count += 1
            result = self._verify_with_model(
                screenshot,
                context,
                expected,
                confidence_threshold,
                use_primary=False
            )
        
        # If both failed, return error result
        if result is None:
            self.error_count += 1
            return VerificationResult(
                safe_to_proceed=False,
                confidence=0.0,
                analysis="Both primary and fallback models failed",
                model_used="none"
            )
        
        return result
    
    def _verify_with_model(
        self,
        screenshot: Image.Image,
        context: str,
        expected: str,
        confidence_threshold: float,
        use_primary: bool = True
    ) -> Optional[VerificationResult]:
        """
        Verify screenshot using specified model.
        
        Args:
            screenshot: PIL Image to analyze
            context: Verification context
            expected: Expected state
            confidence_threshold: Minimum confidence
            use_primary: If True, use primary model; otherwise use fallback
            
        Returns:
            VerificationResult or None if model fails
            
        Requirements:
        - 11.4: Automatic fallback on primary failure
        - 13.3: Timeout handling
        """
        model = self.primary_model if use_primary else self.fallback_model
        model_name = self.primary_model_name if use_primary else self.fallback_model_name
        
        if not model:
            return None
        
        # Build verification prompt
        prompt = self._build_verification_prompt(context, expected, confidence_threshold)
        
        try:
            print(f"  Analyzing with {model_name}...")
            start_time = time.time()
            
            # Send to Gemini vision model
            response = model.generate_content(
                [prompt, screenshot],
                request_options={'timeout': self.timeout_seconds}
            )
            
            elapsed = time.time() - start_time
            print(f"  ✓ Analysis completed in {elapsed:.2f}s")
            
            # Parse response
            result = self._parse_verification_response(
                response.text,
                model_name,
                confidence_threshold
            )
            
            return result
            
        except Exception as e:
            print(f"  ✗ Model {model_name} failed: {str(e)}")
            return None
    
    def _build_verification_prompt(
        self,
        context: str,
        expected: str,
        confidence_threshold: float
    ) -> str:
        """
        Build the prompt for visual verification.
        
        Args:
            context: Verification context
            expected: Expected state
            confidence_threshold: Minimum confidence
            
        Returns:
            Formatted prompt string
        """
        prompt = f"""You are a visual verification AI for desktop automation.

**Context:** {context}
**Expected State:** {expected}
**Confidence Threshold:** {confidence_threshold}

Analyze this screenshot and determine:

1. **Is it safe to proceed?**
   - YES if the expected state is visible and ready for interaction
   - NO if the expected state is not visible, obscured, or not ready

2. **Confidence Level** (0.0 to 1.0)
   - How confident are you in your assessment?

3. **Element Coordinates** (if applicable)
   - If you can identify the target element, provide its approximate center coordinates
   - Coordinates should be in pixels from top-left corner (x, y)

4. **Analysis**
   - Brief description of what you see
   - Why it's safe or not safe to proceed

5. **Suggested Actions** (if not safe to proceed)
   - What actions should be taken instead?
   - Alternative coordinates or approaches?

**Response Format (JSON):**
```json
{{
  "safe_to_proceed": true/false,
  "confidence": 0.0-1.0,
  "analysis": "description of what you see",
  "coordinates": {{"x": 123, "y": 456}},  // Optional, only if element found
  "suggested_actions": ["action1", "action2"]  // Optional, only if not safe
}}
```

**Important:**
- Be conservative: if uncertain, set safe_to_proceed to false
- Only provide coordinates if you're confident about the element location
- Consider visibility, readiness, and accessibility of UI elements
"""
        return prompt
    
    def _parse_verification_response(
        self,
        response_text: str,
        model_name: str,
        confidence_threshold: float
    ) -> VerificationResult:
        """
        Parse the AI vision response into a VerificationResult.
        
        Args:
            response_text: Raw response from Gemini
            model_name: Name of model that generated response
            confidence_threshold: Minimum confidence threshold
            
        Returns:
            VerificationResult with parsed data
            
        Requirements:
        - 11.5: Parse safe_to_proceed vs requires_adaptation
        - 11.6: Extract updated coordinates
        """
        import json
        import re
        
        try:
            # Extract JSON from response (handle markdown code blocks)
            cleaned = response_text.strip()
            if '```json' in cleaned:
                cleaned = cleaned.split('```json')[1].split('```')[0].strip()
            elif '```' in cleaned:
                cleaned = cleaned.split('```')[1].split('```')[0].strip()
            
            # Parse JSON
            data = json.loads(cleaned)
            
            # Extract fields
            safe_to_proceed = data.get('safe_to_proceed', False)
            confidence = float(data.get('confidence', 0.0))
            analysis = data.get('analysis', 'No analysis provided')
            
            # Extract coordinates if provided
            updated_coordinates = None
            if 'coordinates' in data and data['coordinates']:
                coords = data['coordinates']
                if 'x' in coords and 'y' in coords:
                    updated_coordinates = {
                        'x': int(coords['x']),
                        'y': int(coords['y'])
                    }
            
            # Extract suggested actions
            suggested_actions = data.get('suggested_actions', [])
            
            # Apply confidence threshold
            if confidence < confidence_threshold:
                print(f"  ⚠ Confidence {confidence:.2f} below threshold {confidence_threshold}")
                safe_to_proceed = False
            
            # Log result
            status = "✓ SAFE" if safe_to_proceed else "✗ NOT SAFE"
            print(f"  {status} (confidence: {confidence:.2f})")
            print(f"  Analysis: {analysis}")
            if updated_coordinates:
                print(f"  Coordinates: ({updated_coordinates['x']}, {updated_coordinates['y']})")
            
            return VerificationResult(
                safe_to_proceed=safe_to_proceed,
                confidence=confidence,
                analysis=analysis,
                updated_coordinates=updated_coordinates,
                suggested_actions=suggested_actions,
                model_used=model_name
            )
            
        except json.JSONDecodeError as e:
            print(f"  ✗ Failed to parse JSON response: {e}")
            print(f"  Raw response: {response_text[:200]}...")
            
            # Fallback: try to extract basic info from text
            safe_to_proceed = 'safe to proceed' in response_text.lower() and 'not safe' not in response_text.lower()
            
            return VerificationResult(
                safe_to_proceed=safe_to_proceed,
                confidence=0.5,
                analysis=f"Failed to parse structured response. Raw: {response_text[:200]}",
                model_used=model_name
            )
        
        except Exception as e:
            print(f"  ✗ Error parsing response: {e}")
            return VerificationResult(
                safe_to_proceed=False,
                confidence=0.0,
                analysis=f"Error parsing response: {str(e)}",
                model_used=model_name
            )
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get verification statistics.
        
        Returns:
            Dictionary with statistics
        """
        return {
            'total_verifications': self.verification_count,
            'fallback_uses': self.fallback_count,
            'errors': self.error_count,
            'fallback_rate': self.fallback_count / max(1, self.verification_count),
            'error_rate': self.error_count / max(1, self.verification_count),
            'primary_model': self.primary_model_name,
            'fallback_model': self.fallback_model_name
        }
