"""
Test for Task 6: Configure Smooth Mouse Movements

Verifies that MouseController is configured with smooth curved movements by default.

Requirements:
- 12.1: Mouse movements use smooth curved paths by default
- 12.2: Bezier curves are the default curve type
- 12.6: Proper default configuration for curve_intensity, speed, overshoot, and noise
"""

import sys
sys.path.insert(0, '.')

from automation_engine.mouse_controller import MouseController, MouseConfig


def test_mouse_config_defaults():
    """Test that MouseConfig has proper defaults for smooth movements."""
    print("\n" + "=" * 60)
    print("TEST: MouseConfig Default Values")
    print("=" * 60)
    
    config = MouseConfig()
    
    # Verify curve_intensity default
    assert config.curve_intensity == 0.3, f"Expected curve_intensity=0.3, got {config.curve_intensity}"
    print(f"✓ curve_intensity: {config.curve_intensity} (0.0=straight, 1.0=very curved)")
    
    # Verify speed default
    assert config.speed == 1.0, f"Expected speed=1.0, got {config.speed}"
    print(f"✓ speed: {config.speed} (movement speed multiplier)")
    
    # Verify overshoot default
    assert config.overshoot == True, f"Expected overshoot=True, got {config.overshoot}"
    print(f"✓ overshoot: {config.overshoot} (natural human-like overshoot)")
    
    # Verify overshoot_amount default
    assert config.overshoot_amount == 0.05, f"Expected overshoot_amount=0.05, got {config.overshoot_amount}"
    print(f"✓ overshoot_amount: {config.overshoot_amount} (5% of distance)")
    
    # Verify add_noise default
    assert config.add_noise == True, f"Expected add_noise=True, got {config.add_noise}"
    print(f"✓ add_noise: {config.add_noise} (human-like micro-adjustments)")
    
    # Verify noise_amount default
    assert config.noise_amount == 2.0, f"Expected noise_amount=2.0, got {config.noise_amount}"
    print(f"✓ noise_amount: {config.noise_amount} pixels")
    
    print("\n✓ All MouseConfig defaults are properly configured for smooth movements")


def test_mouse_controller_initialization():
    """Test that MouseController initializes with smooth defaults."""
    print("\n" + "=" * 60)
    print("TEST: MouseController Initialization")
    print("=" * 60)
    
    # Initialize without explicit config (should use defaults)
    controller = MouseController()
    
    # Verify config is set
    assert controller.config is not None, "MouseController should have a config"
    print(f"✓ MouseController initialized with config")
    
    # Verify default config values
    assert controller.config.curve_intensity == 0.3, "Should use default curve_intensity"
    assert controller.config.speed == 1.0, "Should use default speed"
    assert controller.config.overshoot == True, "Should use default overshoot"
    assert controller.config.add_noise == True, "Should use default add_noise"
    
    print(f"✓ MouseController uses smooth movement defaults:")
    print(f"  - Curved paths (intensity: {controller.config.curve_intensity})")
    print(f"  - Natural speed (multiplier: {controller.config.speed})")
    print(f"  - Overshoot enabled: {controller.config.overshoot}")
    print(f"  - Noise enabled: {controller.config.add_noise}")


def test_move_to_default_curve_type():
    """Test that move_to uses bezier curve by default."""
    print("\n" + "=" * 60)
    print("TEST: move_to Default Curve Type")
    print("=" * 60)
    
    controller = MouseController()
    
    # Check the move_to method signature
    import inspect
    sig = inspect.signature(controller.move_to)
    
    # Verify curve_type parameter exists and defaults to 'bezier'
    assert 'curve_type' in sig.parameters, "move_to should have curve_type parameter"
    
    curve_type_param = sig.parameters['curve_type']
    assert curve_type_param.default == 'bezier', f"Expected default curve_type='bezier', got {curve_type_param.default}"
    
    print(f"✓ move_to() defaults to curve_type='bezier'")
    print(f"  Available curve types: bezier, arc, wave")
    print(f"  Default: {curve_type_param.default}")


def test_action_handler_smooth_default():
    """Test that mouse_move action handler uses smooth=True by default."""
    print("\n" + "=" * 60)
    print("TEST: Action Handler Smooth Default")
    print("=" * 60)
    
    from shared.action_registry import ActionRegistry
    from shared.action_handlers import ActionHandlers
    
    # Create registry and register handlers
    registry = ActionRegistry()
    handlers = ActionHandlers(registry)
    handlers.register_mouse_handlers()
    
    # Get mouse_move handler
    handler = registry.get_handler("mouse_move")
    assert handler is not None, "mouse_move handler should be registered"
    
    # Check optional params
    assert "smooth" in handler.optional_params, "mouse_move should have smooth parameter"
    assert handler.optional_params["smooth"] == True, "smooth should default to True"
    
    assert "curve_type" in handler.optional_params, "mouse_move should have curve_type parameter"
    assert handler.optional_params["curve_type"] == "bezier", "curve_type should default to 'bezier'"
    
    print(f"✓ mouse_move action handler defaults:")
    print(f"  - smooth: {handler.optional_params['smooth']}")
    print(f"  - curve_type: {handler.optional_params['curve_type']}")
    print(f"  - speed: {handler.optional_params['speed']}")


def test_smooth_movement_configuration_summary():
    """Print summary of smooth movement configuration."""
    print("\n" + "=" * 60)
    print("SMOOTH MOVEMENT CONFIGURATION SUMMARY")
    print("=" * 60)
    
    config = MouseConfig()
    
    print("\n1. CURVE SETTINGS:")
    print(f"   - Default curve type: bezier")
    print(f"   - Curve intensity: {config.curve_intensity} (0.0-1.0)")
    print(f"   - Available types: bezier, arc, wave")
    
    print("\n2. SPEED SETTINGS:")
    print(f"   - Speed multiplier: {config.speed}")
    print(f"   - Min duration: {config.min_duration}s")
    print(f"   - Max duration: {config.max_duration}s")
    
    print("\n3. HUMAN-LIKE BEHAVIOR:")
    print(f"   - Overshoot: {config.overshoot}")
    print(f"   - Overshoot amount: {config.overshoot_amount * 100}%")
    print(f"   - Add noise: {config.add_noise}")
    print(f"   - Noise amount: {config.noise_amount} pixels")
    
    print("\n4. TIMING:")
    print(f"   - Click delay: {config.click_delay_min}-{config.click_delay_max}s")
    
    print("\n5. SAFETY:")
    print(f"   - Boundary margin: {config.boundary_margin} pixels")
    
    print("\n✓ All mouse movements use smooth curved paths by default")
    print("✓ Bezier curves provide natural, human-like motion")
    print("✓ Overshoot and noise add realistic imperfection")


def run_all_tests():
    """Run all tests for Task 6."""
    print("\n" + "=" * 60)
    print("TASK 6: CONFIGURE SMOOTH MOUSE MOVEMENTS")
    print("Testing MouseController Configuration")
    print("=" * 60)
    
    try:
        test_mouse_config_defaults()
        test_mouse_controller_initialization()
        test_move_to_default_curve_type()
        test_action_handler_smooth_default()
        test_smooth_movement_configuration_summary()
        
        print("\n" + "=" * 60)
        print("✓ ALL TESTS PASSED")
        print("=" * 60)
        print("\nTask 6 Requirements Verified:")
        print("  ✓ 12.1: Mouse movements use smooth curved paths by default")
        print("  ✓ 12.2: Bezier curves are the default curve type")
        print("  ✓ 12.6: Proper defaults for curve_intensity, speed, overshoot, noise")
        print("\nTask 6 Implementation: COMPLETE")
        
        return True
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
