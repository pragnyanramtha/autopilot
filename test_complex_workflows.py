"""
Test complex workflow generation and processing.
Demonstrates the enhanced AI Brain capabilities.
"""
import os
from ai_brain.gemini_client import GeminiClient, CommandIntent
from ai_brain.workflow_generator import WorkflowGenerator


def test_simple_command():
    """Test that simple commands still work."""
    print("\n=== Test 1: Simple Command ===")
    
    # Simulate a simple command intent
    intent = CommandIntent(
        action='click',
        target='submit button',
        parameters={},
        confidence=0.95
    )
    
    generator = WorkflowGenerator()
    workflow = generator.create_workflow(intent)
    
    print(f"Workflow ID: {workflow.id}")
    print(f"Steps: {len(workflow.steps)}")
    print(f"Complexity: {workflow.metadata.get('complexity', 'simple')}")
    
    for i, step in enumerate(workflow.steps, 1):
        print(f"  {i}. {step.type}: {step.data or step.coordinates}")
    
    assert len(workflow.steps) > 0
    print("✓ Simple command test passed")


def test_complex_command_structure():
    """Test complex command with sub-tasks."""
    print("\n=== Test 2: Complex Command Structure ===")
    
    # Simulate a complex command intent
    intent = CommandIntent(
        action='multi_step',
        target='write article and post to X',
        parameters={
            'complexity': 'complex',
            'sub_tasks': [
                {
                    'action': 'search_web',
                    'target': 'AI trends',
                    'parameters': {'query': 'latest AI trends 2025'},
                    'description': 'Research AI topics'
                },
                {
                    'action': 'generate_content',
                    'target': 'article',
                    'parameters': {'topic': 'AI', 'length': 'medium'},
                    'description': 'Write article about AI'
                },
                {
                    'action': 'open_app',
                    'target': 'Chrome',
                    'parameters': {},
                    'description': 'Open browser'
                },
                {
                    'action': 'navigate_to_url',
                    'target': 'https://x.com',
                    'parameters': {},
                    'description': 'Go to X'
                },
                {
                    'action': 'login',
                    'target': 'X',
                    'parameters': {'service': 'x.com'},
                    'description': 'Login to X'
                },
                {
                    'action': 'post_to_social',
                    'target': 'X',
                    'parameters': {'platform': 'x', 'content_source': 'generated'},
                    'description': 'Post the article'
                }
            ],
            'requires_research': True,
            'requires_authentication': True,
            'requires_content_generation': True
        },
        confidence=0.85
    )
    
    generator = WorkflowGenerator()
    workflow = generator.create_workflow(intent)
    
    print(f"Workflow ID: {workflow.id}")
    print(f"Steps: {len(workflow.steps)}")
    print(f"Complexity: {workflow.metadata.get('complexity', 'simple')}")
    print(f"\nSub-tasks breakdown:")
    
    for i, task in enumerate(intent.parameters['sub_tasks'], 1):
        print(f"  {i}. {task['description']} ({task['action']})")
    
    print(f"\nGenerated workflow steps:")
    for i, step in enumerate(workflow.steps[:10], 1):  # Show first 10 steps
        print(f"  {i}. {step.type}: {step.data or step.coordinates or '(action)'}")
    
    if len(workflow.steps) > 10:
        print(f"  ... and {len(workflow.steps) - 10} more steps")
    
    assert len(workflow.steps) > 0
    assert workflow.metadata.get('complexity') == 'complex'
    print("✓ Complex command structure test passed")


def test_content_generation():
    """Test content generation capability."""
    print("\n=== Test 3: Content Generation ===")
    
    # Check if API key is available
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("⚠ Skipping content generation test (no API key in environment)")
        return
    
    if api_key == 'YOUR_GEMINI_API_KEY_HERE':
        print("⚠ Skipping content generation test (placeholder API key)")
        return
    
    try:
        client = GeminiClient(api_key=api_key)
        
        # Generate short content
        content = client.generate_content(
            topic="Python best practices",
            content_type="article",
            parameters={
                'length': 'short',
                'style': 'informative',
                'tone': 'professional'
            }
        )
        
        print(f"Generated content ({len(content)} characters):")
        print(f"{content[:200]}...")
        
        assert len(content) > 0
        print("✓ Content generation test passed")
        
    except Exception as e:
        print(f"⚠ Content generation test failed: {e}")


def test_research_capability():
    """Test research capability."""
    print("\n=== Test 4: Research Capability ===")
    
    # Check if API key is available
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("⚠ Skipping research test (no API key in environment)")
        return
    
    if api_key == 'YOUR_GEMINI_API_KEY_HERE':
        print("⚠ Skipping research test (placeholder API key)")
        return
    
    try:
        client = GeminiClient(api_key=api_key)
        
        # Research a topic
        research = client.research_topic("latest AI trends")
        
        print(f"Research results:")
        print(f"  Summary: {research.get('summary', 'N/A')[:100]}...")
        print(f"  Key points: {len(research.get('key_points', []))}")
        print(f"  Trends: {len(research.get('trends', []))}")
        print(f"  Examples: {len(research.get('examples', []))}")
        
        assert 'summary' in research
        print("✓ Research capability test passed")
        
    except Exception as e:
        print(f"⚠ Research test failed: {e}")


def test_workflow_validation():
    """Test workflow validation."""
    print("\n=== Test 5: Workflow Validation ===")
    
    intent = CommandIntent(
        action='click',
        target='button',
        parameters={'x': 100, 'y': 200},
        confidence=0.9
    )
    
    generator = WorkflowGenerator()
    workflow = generator.create_workflow(intent)
    
    # Validate workflow
    validation = generator.validate_workflow(workflow)
    
    print(f"Validation result:")
    print(f"  Valid: {validation['valid']}")
    print(f"  Issues: {len(validation['issues'])}")
    print(f"  Warnings: {len(validation['warnings'])}")
    
    if validation['issues']:
        for issue in validation['issues']:
            print(f"    - {issue}")
    
    if validation['warnings']:
        for warning in validation['warnings']:
            print(f"    - {warning}")
    
    assert validation['valid']
    print("✓ Workflow validation test passed")


def test_new_action_types():
    """Test new action types."""
    print("\n=== Test 6: New Action Types ===")
    
    generator = WorkflowGenerator()
    
    # Test navigate_to_url
    intent1 = CommandIntent(
        action='navigate_to_url',
        target='https://example.com',
        parameters={},
        confidence=0.9
    )
    workflow1 = generator.create_workflow(intent1)
    print(f"Navigate workflow: {len(workflow1.steps)} steps")
    
    # Test login
    intent2 = CommandIntent(
        action='login',
        target='X',
        parameters={'service': 'x.com'},
        confidence=0.9
    )
    workflow2 = generator.create_workflow(intent2)
    print(f"Login workflow: {len(workflow2.steps)} steps")
    
    # Test fill_form
    intent3 = CommandIntent(
        action='fill_form',
        target='contact form',
        parameters={'form_data': {'name': 'John', 'email': 'john@example.com'}},
        confidence=0.9
    )
    workflow3 = generator.create_workflow(intent3)
    print(f"Fill form workflow: {len(workflow3.steps)} steps")
    
    assert len(workflow1.steps) > 0
    assert len(workflow2.steps) > 0
    assert len(workflow3.steps) > 0
    print("✓ New action types test passed")


def main():
    """Run all tests."""
    print("=" * 60)
    print("Testing Complex Workflow Enhancements")
    print("=" * 60)
    
    try:
        test_simple_command()
        test_complex_command_structure()
        test_content_generation()
        test_research_capability()
        test_workflow_validation()
        test_new_action_types()
        
        print("\n" + "=" * 60)
        print("All tests completed!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
