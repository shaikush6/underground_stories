#!/usr/bin/env python3
"""
Test API Methods
================

Quick test to verify all methods exist in the Underground API.
"""

import sys
from pathlib import Path

# Add project paths
sys.path.append(str(Path(__file__).parent))

def test_api_methods():
    """Test that all expected methods exist in the API"""
    print("🔍 Testing Underground API method availability...")
    
    try:
        from packages.core.api.underground_api import get_underground_api
        
        api = get_underground_api()
        
        # Check if the method exists
        methods_to_check = [
            'generate_minute_myths_video',
            'generate_blueprint', 
            'get_system_health',
            'get_production_status'
        ]
        
        for method_name in methods_to_check:
            if hasattr(api, method_name):
                method = getattr(api, method_name)
                print(f"✅ {method_name}: {type(method)}")
            else:
                print(f"❌ {method_name}: MISSING")
        
        # Get all methods for debugging
        all_methods = [m for m in dir(api) if not m.startswith('_')]
        print(f"\n📋 All available methods ({len(all_methods)}):")
        for method in sorted(all_methods):
            print(f"   - {method}")
            
    except Exception as e:
        print(f"❌ Error testing API: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_api_methods()