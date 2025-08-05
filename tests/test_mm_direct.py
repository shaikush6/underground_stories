#!/usr/bin/env python3
"""
Test Minute Myths Direct Call
=============================

Test calling the exact same method the web app calls.
"""

import asyncio
import sys
from pathlib import Path

# Add project paths
sys.path.append(str(Path(__file__).parent))

async def test_mm_direct():
    """Test calling the API method directly like the web app does"""
    print("🔍 Testing direct MM API call...")
    
    try:
        from packages.core.api.underground_api import get_underground_api
        
        api = get_underground_api()
        print(f"✅ API instance created: {type(api)}")
        
        # Check if method exists
        if hasattr(api, 'generate_minute_myths_video'):
            print("✅ Method 'generate_minute_myths_video' exists")
            method = getattr(api, 'generate_minute_myths_video')
            print(f"✅ Method type: {type(method)}")
            
            # Test the exact call the web app makes
            print("🎬 Calling generate_minute_myths_video...")
            result = await api.generate_minute_myths_video(
                myth_name="Perseus and Medusa",
                mythology_category="Greek Mythology", 
                video_format="Single Video",
                narration_style="Epic"
            )
            
            print(f"📊 Result: {result}")
            
        else:
            print("❌ Method NOT found!")
            print("Available methods:")
            methods = [m for m in dir(api) if not m.startswith('_')]
            for method in sorted(methods):
                print(f"   - {method}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_mm_direct())