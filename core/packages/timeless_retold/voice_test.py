#!/usr/bin/env python3
"""
Quick voice test for Timeless Retold
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add packages to path
sys.path.append(str(Path(__file__).parent.parent))

from timeless_retold.timeless_adapter import TimelessRetoldAdapter

async def test_voice():
    logging.basicConfig(level=logging.INFO)
    
    adapter = TimelessRetoldAdapter()
    
    test_text = """In the heart of Victorian London, where gas lamps flickered through perpetual fog, extraordinary adventures awaited those brave enough to seek them. This is a voice quality test of our Timeless Retold pipeline, featuring Google's premium Wavenet-D voice for sophisticated literary narration."""
    
    result = await adapter.process_classic_text(
        text=test_text,
        title="Voice Test Sample",
        author="Underground Stories", 
        chapter="Voice Quality Test",
        job_id="voice_sample_test"
    )
    
    if result["success"]:
        print(f"✅ Generated: {result['audio_path']}")
        print(f"Duration: {result['duration_seconds']:.1f}s")
        print(f"Cost: {result['cost_cents']}¢")
    else:
        print(f"❌ Failed: {result.get('error', 'Unknown')}")

if __name__ == "__main__":
    asyncio.run(test_voice())