# Mouse Movement Visualization

## Movement Path Comparison

### Traditional (Straight Line)
```
Start Point (100, 100)
    │
    │  Direct path - robotic
    │  No acceleration
    │  Instant direction change
    │  Obvious automation
    ↓
End Point (500, 300)
```

### Advanced (Bezier Curve)
```
Start Point (100, 100)
    ╲
     ╲  Smooth curve
      ╲  Natural acceleration
       ╲  Gradual direction change
        ╲  Human-like movement
         ╲
          ╲
           ↘
            End Point (500, 300)
```

## Bezier Curve Path Generation

### Control Points
```
                    CP2 (450, 250)
                      ●
                    ╱   ╲
                  ╱       ╲
                ╱           ╲
              ╱               ╲
Start ●────●                   ●────● End
(100,100) CP1                      (500,300)
         (200,150)

Path follows smooth curve through control points
```

### Path with Overshoot
```
                        Overshoot
                           ●
                         ╱  ╲
                       ╱     ╲ Correction
                     ╱        ↓
Start ●───────────╱          ● Target
                            (500,300)

1. Move along curve
2. Slightly overshoot target
3. Correct back to exact position
```

## Movement Phases

### Phase 1: Acceleration (0-33%)
```
Speed: ▁▂▃▄▅
       Slow → Fast

Start ●─────────────────────────────────────
       ╲
        ╲  Gradual speed increase
         ╲  Smooth acceleration
          ╲  Natural feel
```

### Phase 2: Constant Speed (33-66%)
```
Speed: ▅▅▅▅▅
       Fast → Fast

           ╲
            ╲  Maintaining speed
             ╲  Smooth trajectory
              ╲  Efficient movement
```

### Phase 3: Deceleration (66-100%)
```
Speed: ▅▄▃▂▁
       Fast → Slow

                ╲
                 ╲  Gradual slowdown
                  ╲  Smooth deceleration
                   ╲  Precise landing
                    ● End
```

## Curve Types Visualization

### 1. Bezier Curve (Default)
```
Start ●
       ╲
        ╲
         ╲
          ╲
           ╲
            ╲
             ● End

Characteristics:
• S-shaped curve
• Natural acceleration
• Most human-like
```

### 2. Arc Path
```
Start ●
       ╲
        ╲╲
          ╲╲
            ╲╲
              ╲● End

Characteristics:
• Circular arc
• Consistent curvature
• Sweeping motion
```

### 3. Wave Path
```
Start ●
       ╲  ╱╲  ╱╲
        ╲╱  ╲╱  ╲
              ╲  ● End

Characteristics:
• Oscillating path
• Wave-like motion
• Unique effect
```

## Noise Addition

### Without Noise (Perfect Path)
```
Start ●─────────────────────────● End
       Perfect straight line
       Looks robotic
```

### With Noise (Human-like)
```
Start ●─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─● End
       ╲ ╱ ╲ ╱ ╲ ╱ ╲ ╱ ╲ ╱
        Micro-adjustments
        Looks natural
```

## Curve Intensity Comparison

### Intensity: 0.0 (Straight)
```
Start ●──────────────────────────● End
```

### Intensity: 0.3 (Subtle - Default)
```
Start ●
       ╲
        ╲
         ╲
          ● End
```

### Intensity: 0.7 (Obvious)
```
Start ●
       ╲
        ╲
         ╲
          ╲
           ╲
            ╲
             ● End
```

### Intensity: 1.0 (Extreme)
```
Start ●
       ╲
        ╲
         ╲
          ╲
           ╲
            ╲
             ╲
              ╲
               ● End
```

## Speed Comparison

### Speed: 0.5x (Slow)
```
Time: ████████████████████████
      0s                    2s

Start ●─────────────────────● End
       Very slow, deliberate
```

### Speed: 1.0x (Normal)
```
Time: ████████████
      0s        1s

Start ●───────────● End
       Natural speed
```

### Speed: 2.0x (Fast)
```
Time: ██████
      0s  0.5s

Start ●─────● End
       Quick movement
```

## Click Operation Timeline

```
Time:  0ms    50ms   100ms  150ms  200ms
       │      │      │      │      │
       │      │      │      │      │
Move   ████████████████            │
       │      │      │      │      │
Delay  │      │      ██████        │
       │      │      │      │      │
Click  │      │      │      ████   │
       │      │      │      │      │
       Start  │      │      │      Done
              │      │      │
              Move   Wait   Click
              Done   Random
```

## Drag Operation

### Drag Path
```
Start Position
    ●
    │ Press button down
    │
    ├─────────────────────┐
    │                     │
    │  Smooth curved path │
    │  Button held down   │
    │                     │
    └─────────────────────┤
                          │
                          ● End Position
                          │ Release button
```

## Real-World Example: Form Filling

```
Screen Layout:
┌─────────────────────────────────────┐
│  Form                               │
│                                     │
│  Name:    [____________] ← Field 1  │
│                                     │
│  Email:   [____________] ← Field 2  │
│                                     │
│  Message: [____________] ← Field 3  │
│                                     │
│           [  Submit  ]   ← Button   │
│                                     │
└─────────────────────────────────────┘

Mouse Path:
    Start
      ●
       ╲
        ╲ Curve to Field 1
         ● Click
          │
          ╲
           ╲ Curve to Field 2
            ● Click
             │
             ╲
              ╲ Curve to Field 3
               ● Click
                │
                ╲
                 ╲ Curve to Submit
                  ● Click
                   │
                  Done
```

## Performance Visualization

### Path Generation Process
```
Input: Start (100,100), End (500,300)
  │
  ├─ Calculate distance: 447 pixels
  │
  ├─ Calculate duration: 0.45 seconds
  │
  ├─ Generate control points
  │   CP1: (200, 150)
  │   CP2: (450, 250)
  │
  ├─ Calculate 27 points (60 FPS × 0.45s)
  │   Point 1: (100, 100) at 0.000s
  │   Point 2: (108, 103) at 0.017s
  │   Point 3: (117, 107) at 0.033s
  │   ...
  │   Point 27: (500, 300) at 0.450s
  │
  ├─ Apply easing function to each point
  │
  ├─ Add random noise (±2 pixels)
  │
  └─ Add overshoot if enabled
      Point 28: (505, 302) at 0.500s
      Point 29: (500, 300) at 0.600s

Output: 29 points ready for execution
Time: ~5ms
```

## Memory Layout

```
MouseController Instance
├─ config: MouseConfig (256 bytes)
├─ screen_width: int (8 bytes)
├─ screen_height: int (8 bytes)
└─ Total: ~300 bytes

Path Data (per movement)
├─ points: List[Tuple] (27 points × 24 bytes)
├─ timestamps: List[float] (27 × 8 bytes)
└─ Total: ~864 bytes ≈ 1 KB

Total Memory per Movement: ~1 KB
```

## Coordinate System

```
Screen Coordinates:
(0,0) ────────────────────────── (width,0)
  │                                  │
  │                                  │
  │         Screen Area              │
  │                                  │
  │                                  │
  │                                  │
(0,height) ──────────────── (width,height)

Safe Zone (with 5px margin):
(5,5) ────────────────────── (width-5,5)
  │                              │
  │    Safe Movement Area        │
  │                              │
(5,height-5) ────────── (width-5,height-5)
```

## Easing Function Graph

```
Speed
  │
1.0│         ╭─────────╮
   │       ╱           ╲
   │      ╱             ╲
0.5│    ╱                 ╲
   │   ╱                   ╲
   │  ╱                     ╲
0.0│─╯                       ╰─
   └─────────────────────────────→ Time
   0%   25%   50%   75%   100%

Cubic Ease-In-Out:
• Slow start (ease in)
• Fast middle (constant)
• Slow end (ease out)
```

## Comparison Chart

```
Feature          │ Straight │ Bezier │ Arc  │ Wave
─────────────────┼──────────┼────────┼──────┼──────
Natural Look     │    ★     │  ★★★★★ │ ★★★★ │ ★★★
Speed            │  ★★★★★   │  ★★★★  │ ★★★★ │ ★★★
Precision        │  ★★★★★   │  ★★★★  │ ★★★  │ ★★
CPU Usage        │    ★     │  ★★    │ ★★   │ ★★★
Human-like       │    ★     │  ★★★★★ │ ★★★★ │ ★★★
Predictability   │  ★★★★★   │  ★★★   │ ★★★★ │ ★★
```

## Algorithm Complexity

```
Path Generation:
├─ Distance Calculation: O(1)
├─ Control Points: O(1)
├─ Bezier Points: O(n) where n = frame_count
├─ Easing Application: O(n)
├─ Noise Addition: O(n)
└─ Total: O(n) ≈ O(60) for 1 second

Execution:
├─ Move to Point: O(1) per point
├─ Sleep: O(1) per point
└─ Total: O(n) ≈ O(60) for 1 second

Overall: Linear time complexity
Very efficient for real-time use
```

## State Machine

```
Mouse Controller States:

    ┌─────────┐
    │  IDLE   │
    └────┬────┘
         │
         │ move_to() called
         ↓
    ┌─────────┐
    │GENERATE │ ← Calculate path
    │  PATH   │   (~5ms)
    └────┬────┘
         │
         │ path ready
         ↓
    ┌─────────┐
    │ MOVING  │ ← Execute movement
    │         │   (0.3-1.5s)
    └────┬────┘
         │
         │ movement complete
         ↓
    ┌─────────┐
    │  IDLE   │
    └─────────┘
```

## Error Handling Flow

```
User Input: move_to(x, y)
    │
    ├─ Validate coordinates
    │   ├─ x < 0? → Clamp to margin
    │   ├─ x > width? → Clamp to width-margin
    │   ├─ y < 0? → Clamp to margin
    │   └─ y > height? → Clamp to height-margin
    │
    ├─ Generate path
    │   └─ Check for errors
    │       └─ Fail? → Raise exception
    │
    ├─ Execute movement
    │   ├─ Check fail-safe
    │   │   └─ Triggered? → Stop immediately
    │   │
    │   └─ Move to each point
    │       └─ Error? → Stop and report
    │
    └─ Complete
        └─ Return success
```

---

**Visual representations help understand the smooth, natural movements of the advanced mouse control system!**
