# System Architecture - AI Automation Assistant

## Overview

This document describes the complete system architecture for the AI Automation Assistant, including the advanced mouse control system with smooth curved movements.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ Text Input   │  │ Voice Input  │  │  Web UI      │         │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘         │
└─────────┼──────────────────┼──────────────────┼────────────────┘
          │                  │                  │
          └──────────────────┴──────────────────┘
                             │
┌────────────────────────────┴────────────────────────────────────┐
│                        AI BRAIN LAYER                           │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Gemini Client (LLM Interface)               │  │
│  │  • Command Processing    • Intent Recognition            │  │
│  │  • Content Generation    • Context Management            │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Workflow Generator                          │  │
│  │  • Workflow Creation     • Step Sequencing               │  │
│  │  • Parameter Validation  • Complexity Analysis           │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────┴────────────────────────────────────┐
│                   AUTOMATION ENGINE LAYER                       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Automation Executor                         │  │
│  │  • Workflow Execution    • Safety Monitoring             │  │
│  │  • Error Handling        • State Management              │  │
│  │  • Pause/Resume/Stop     • Progress Tracking             │  │
│  └──────────────┬───────────────────────────────────────────┘  │
│                 │                                               │
│  ┌──────────────┴───────────────────────────────────────────┐  │
│  │              Input Controller                            │  │
│  │  • Mouse Control         • Keyboard Control              │  │
│  │  • Click Management      • Hotkey Support                │  │
│  └──────────────┬───────────────────────────────────────────┘  │
│                 │                                               │
│  ┌──────────────┴───────────────────────────────────────────┐  │
│  │         Advanced Mouse Controller (NEW)                  │  │
│  │  ┌────────────────────────────────────────────────────┐  │  │
│  │  │  Path Generation                                   │  │  │
│  │  │  • Bezier Curves      • Arc Paths                  │  │  │
│  │  │  • Wave Patterns      • Custom Curves              │  │  │
│  │  └────────────────────────────────────────────────────┘  │  │
│  │  ┌────────────────────────────────────────────────────┐  │  │
│  │  │  Movement Features                                 │  │  │
│  │  │  • Smooth Curves      • Easing Functions           │  │  │
│  │  │  • Overshoot/Correct  • Random Noise               │  │  │
│  │  │  • Speed Control      • Boundary Safety            │  │  │
│  │  └────────────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Screen Capture                              │  │
│  │  • Full Screen Capture   • Region Capture                │  │
│  │  • Screenshot Storage    • Image Processing              │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────┴────────────────────────────────────┐
│                      SYSTEM LAYER                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   PyAutoGUI  │  │     MSS      │  │    NumPy     │         │
│  │ (Low-level)  │  │ (Capture)    │  │  (Math)      │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└─────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. AI Brain Layer

#### Gemini Client
- **Purpose**: Interface with Google's Gemini AI models
- **Responsibilities**:
  - Process natural language commands
  - Recognize user intent
  - Generate content (tweets, posts, etc.)
  - Maintain conversation context
- **Models**:
  - `gemini-2.5-flash`: Fast, simple tasks
  - `gemini-2.5-pro`: Complex reasoning tasks

#### Workflow Generator
- **Purpose**: Convert AI intent into executable workflows
- **Responsibilities**:
  - Create workflow steps from intent
  - Sequence actions logically
  - Validate parameters
  - Handle complex multi-step tasks

### 2. Automation Engine Layer

#### Automation Executor
- **Purpose**: Execute workflows with safety controls
- **Key Features**:
  - Sequential step execution
  - Pause/Resume/Stop controls
  - Error handling and recovery
  - Progress tracking
  - Safety monitoring (mouse movement detection)
  - Dry-run mode for testing

#### Input Controller
- **Purpose**: High-level interface for input control
- **Capabilities**:
  - Mouse movement (smooth or direct)
  - Click operations (left, right, middle)
  - Keyboard typing
  - Hotkey combinations
  - Position tracking

#### Advanced Mouse Controller (NEW)
- **Purpose**: Provide human-like mouse movements
- **Key Features**:

##### Path Generation Algorithms

1. **Bezier Curves** (Default)
   - Uses cubic Bezier curves for smooth paths
   - Control points calculated based on curve intensity
   - Most natural-looking movement
   ```
   Start → Control Point 1 → Control Point 2 → End
   ```

2. **Arc Paths**
   - Follows circular arc between points
   - Good for sweeping motions
   - Adjustable arc height

3. **Wave Patterns**
   - Adds sinusoidal wave to linear path
   - Creates oscillating movement
   - Useful for specific effects

##### Movement Features

1. **Easing Functions**
   - Cubic ease-in-out for acceleration/deceleration
   - Natural start and stop
   - Mimics human muscle control

2. **Overshoot & Correction**
   - Slightly overshoots target
   - Corrects back to exact position
   - Mimics human aiming behavior

3. **Random Noise**
   - Adds micro-adjustments during movement
   - Prevents perfectly straight lines
   - Makes movement more human-like

4. **Speed Control**
   - Auto-calculates duration based on distance
   - Configurable speed multiplier
   - Min/max duration limits

5. **Boundary Safety**
   - Clamps coordinates to screen bounds
   - Maintains margin from edges
   - Prevents off-screen movements

##### Configuration Options

```python
MouseConfig(
    curve_intensity=0.3,      # 0.0 = straight, 1.0 = very curved
    speed=1.0,                # Movement speed multiplier
    overshoot=True,           # Enable overshoot behavior
    overshoot_amount=0.05,    # Overshoot percentage
    add_noise=True,           # Add random variations
    noise_amount=2.0,         # Noise in pixels
    min_duration=0.3,         # Min movement time (seconds)
    max_duration=1.5,         # Max movement time (seconds)
    click_delay_min=0.05,     # Min delay before click
    click_delay_max=0.15,     # Max delay before click
    boundary_margin=5         # Pixels from screen edge
)
```

#### Screen Capture
- **Purpose**: Capture screen content for analysis
- **Capabilities**:
  - Full screen capture
  - Region capture
  - Screenshot storage
  - Image processing

### 3. Communication Layer

#### Message Broker
- **Purpose**: Inter-component communication
- **Methods**:
  - File-based queues
  - JSON message format
  - Workflow and status queues

### 4. Data Models

#### Workflow
```python
{
    "id": "unique_id",
    "name": "Workflow Name",
    "steps": [...],
    "metadata": {
        "generated_content": "...",
        "complexity": "simple|complex"
    }
}
```

#### WorkflowStep
```python
{
    "type": "mouse_move|click|type|...",
    "coordinates": [x, y],
    "data": "text or command",
    "delay_ms": 100,
    "validation": {...}
}
```

## Mouse Movement Flow

```
User Command: "Click the submit button"
         ↓
AI Brain: Identifies target coordinates (500, 300)
         ↓
Workflow Generator: Creates click step
         ↓
Automation Executor: Executes step
         ↓
Input Controller: Calls mouse.click(500, 300)
         ↓
Mouse Controller:
  1. Get current position (100, 100)
  2. Calculate distance: 447 pixels
  3. Calculate duration: 0.45 seconds
  4. Generate Bezier path:
     - Calculate control points
     - Generate 27 points (60 FPS × 0.45s)
     - Apply easing to each point
     - Add random noise
  5. Add overshoot:
     - Overshoot to (505, 302)
     - Correct to (500, 300)
  6. Execute path:
     - Move through each point
     - Maintain timing
  7. Perform click with delay
         ↓
PyAutoGUI: Low-level mouse control
         ↓
Operating System: Physical mouse movement
```

## Configuration System

### config.json
```json
{
  "gemini": {
    "simple_model": "gemini-2.5-flash",
    "complex_model": "gemini-2.5-pro",
    "temperature": 0.7
  },
  "automation": {
    "safety_delay_ms": 100,
    "enable_safety_monitor": true,
    "interrupt_on_mouse_move": true,
    "mouse_movement": {
      "use_smooth": true,
      "curve_type": "bezier",
      "curve_intensity": 0.3,
      "speed": 1.0,
      "overshoot": true,
      "add_noise": true
    }
  }
}
```

### dev.bat Configuration
Developer mode script with customizable settings:
- AI model selection
- Temperature control
- Automation parameters
- Safety features
- Debug options

## Safety Features

### 1. Emergency Stop
- Move mouse to upper-left corner
- Triggers PyAutoGUI fail-safe
- Immediately halts execution

### 2. Mouse Movement Detection
- Monitors initial mouse position
- Detects user movement (>50 pixels)
- Auto-stops execution if detected

### 3. Boundary Protection
- Clamps all coordinates to screen
- Maintains margin from edges
- Prevents off-screen movements

### 4. Dangerous Action Detection
- Scans commands for dangerous keywords
- Requires confirmation for risky actions
- Blocks in dry-run mode

### 5. Dry-Run Mode
- Simulates execution without actions
- Logs all operations
- Safe for testing

## Performance Characteristics

### Mouse Movement Performance
- **Frame Rate**: 60 FPS path generation
- **Typical Duration**: 0.3 - 1.5 seconds
- **Path Points**: 18 - 90 points per movement
- **Overhead**: ~5ms for path calculation
- **Smoothness**: Cubic Bezier interpolation

### Memory Usage
- Base: ~50 MB
- Per workflow: ~1 MB
- Mouse path: ~10 KB per movement

### CPU Usage
- Idle: <1%
- Path generation: 2-5%
- Movement execution: 1-3%
- AI processing: 10-30% (during API calls)

## Extension Points

### Adding New Movement Types
1. Create method in `MouseController`
2. Add to `curve_type` parameter
3. Implement path generation algorithm
4. Update documentation

### Adding New Step Types
1. Define in `WorkflowStep` type
2. Add execution method in `AutomationExecutor`
3. Update workflow generator
4. Add validation logic

### Custom Easing Functions
1. Add method to `MouseController`
2. Apply in path generation
3. Configure via `MouseConfig`

## Dependencies

### Core
- `google-generativeai`: AI model interface
- `pyautogui`: Low-level input control
- `numpy`: Mathematical operations
- `mss`: Screen capture

### Optional
- `SpeechRecognition`: Voice input
- `PyAudio`: Audio processing
- `pyperclip`: Clipboard operations

## Future Enhancements

### Planned Features
1. **Visual Target Detection**
   - OCR for text recognition
   - Image matching for buttons
   - AI-powered element detection

2. **Advanced Path Planning**
   - Obstacle avoidance
   - Multi-target optimization
   - Context-aware movements

3. **Learning System**
   - Record user movements
   - Learn preferred paths
   - Adapt to user style

4. **Multi-Monitor Support**
   - Cross-screen movements
   - Monitor detection
   - Coordinate translation

5. **Gesture Recognition**
   - Complex mouse gestures
   - Drawing patterns
   - Signature simulation

## Troubleshooting

### Mouse Movements Too Fast
- Decrease `speed` in `MouseConfig`
- Increase `min_duration`

### Mouse Movements Too Curved
- Decrease `curve_intensity`
- Use `arc` or `wave` curve type

### Movements Not Smooth
- Check system performance
- Reduce `noise_amount`
- Disable `overshoot`

### Clicks Missing Target
- Increase `click_delay_min`
- Disable `overshoot`
- Use direct movement mode

## Security Considerations

1. **API Key Protection**
   - Store in `.env` file
   - Never commit to version control
   - Use environment variables

2. **Action Validation**
   - Dangerous action detection
   - User confirmation required
   - Dry-run testing

3. **Screen Capture Privacy**
   - Temporary storage only
   - Automatic cleanup
   - No cloud upload

4. **Input Control Safety**
   - Fail-safe mechanism
   - Boundary protection
   - User interrupt detection

## License & Credits

This system uses:
- Google Gemini AI (Google LLC)
- PyAutoGUI (Al Sweigart)
- NumPy (NumPy Developers)
- MSS (Python MSS Developers)

Bezier curve implementation inspired by:
- De Casteljau's algorithm
- Computer graphics literature
- Human-computer interaction research
