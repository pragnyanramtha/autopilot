"""
Validation script for example protocols.

This script validates all example protocols to ensure they:
1. Are valid JSON
2. Pass protocol schema validation
3. Have valid action names
4. Have valid macro references
5. Have proper variable substitution syntax
"""

import json
import sys
from pathlib import Path

# Add parent directory to path to import shared modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from shared.protocol_parser import JSONProtocolParser
from shared.protocol_models import ProtocolSchema


def validate_protocol_file(filepath: str) -> dict:
    """Validate a single protocol file."""
    print(f"\n{'='*60}")
    print(f"Validating: {filepath}")
    print(f"{'='*60}")
    
    try:
        # Load JSON
        with open(filepath, 'r', encoding='utf-8') as f:
            protocol_json = json.load(f)
        print("✓ Valid JSON")
        
        # Parse with protocol parser
        parser = JSONProtocolParser()
        protocol = parser.parse_dict(protocol_json)
        print("✓ Valid protocol schema")
        
        # Validate protocol
        validation_result = parser.validate_protocol(protocol)
        if not validation_result.is_valid:
            print(f"✗ Validation errors: {validation_result.errors}")
            raise Exception(f"Protocol validation failed: {validation_result.errors}")
        print("✓ Protocol validation passed")
        
        # Display metadata
        print(f"\nMetadata:")
        print(f"  Description: {protocol.metadata.description}")
        print(f"  Complexity: {protocol.metadata.complexity}")
        print(f"  Uses Vision: {protocol.metadata.uses_vision}")
        print(f"  Estimated Duration: {protocol.metadata.estimated_duration_seconds}s")
        
        # Display macro count
        if protocol.macros:
            print(f"\nMacros: {len(protocol.macros)}")
            for macro_name in protocol.macros.keys():
                print(f"  - {macro_name}")
        
        # Display action count
        print(f"\nActions: {len(protocol.actions)}")
        
        # Count action types
        action_types = {}
        for action in protocol.actions:
            action_type = action.action
            action_types[action_type] = action_types.get(action_type, 0) + 1
        
        print("\nAction breakdown:")
        for action_type, count in sorted(action_types.items()):
            print(f"  - {action_type}: {count}")
        
        return {
            'valid': True,
            'filepath': filepath,
            'protocol': protocol
        }
        
    except json.JSONDecodeError as e:
        print(f"✗ JSON Error: {e}")
        return {'valid': False, 'filepath': filepath, 'error': str(e)}
    except Exception as e:
        print(f"✗ Validation Error: {e}")
        return {'valid': False, 'filepath': filepath, 'error': str(e)}


def main():
    """Validate all example protocols."""
    examples_dir = Path(__file__).parent
    
    protocol_files = [
        'simple_search.json',
        'twitter_post.json',
        'visual_verification_workflow.json',
        'complex_macro_workflow.json'
    ]
    
    results = []
    
    print("="*60)
    print("PROTOCOL EXAMPLES VALIDATION")
    print("="*60)
    
    for filename in protocol_files:
        filepath = examples_dir / filename
        if filepath.exists():
            result = validate_protocol_file(str(filepath))
            results.append(result)
        else:
            print(f"\n✗ File not found: {filepath}")
            results.append({'valid': False, 'filepath': str(filepath), 'error': 'File not found'})
    
    # Summary
    print(f"\n{'='*60}")
    print("VALIDATION SUMMARY")
    print(f"{'='*60}")
    
    valid_count = sum(1 for r in results if r['valid'])
    total_count = len(results)
    
    print(f"\nTotal: {total_count}")
    print(f"Valid: {valid_count}")
    print(f"Invalid: {total_count - valid_count}")
    
    if valid_count == total_count:
        print("\n✓ All example protocols are valid!")
        return 0
    else:
        print("\n✗ Some protocols failed validation")
        return 1


if __name__ == '__main__':
    sys.exit(main())
