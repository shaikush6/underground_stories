#!/usr/bin/env python3
"""
Quick Pipeline Test - Core Functionality Only
===========================================

Tests all 3 pipelines without waiting for long DALL-E generation times.
"""

import asyncio
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def quick_test_timeless_retold():
    """Quick test of Timeless Retold core functionality"""
    logger.info("📚 Quick Test: Timeless Retold Core Functions")
    
    try:
        # Check if we have modernized content
        test_chapter = Path("output/text/chapter_01_modernized.txt")
        if not test_chapter.exists():
            logger.warning("⚠️ No modernized content found - skipping Timeless test")
            return False
        
        from packages.timeless_retold.video_generator import TimelessVideoGenerator
        
        generator = TimelessVideoGenerator()
        
        # Read test content  
        with open(test_chapter, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Test scene detection
        scenes = await generator._detect_scenes(content, 1)
        logger.info(f"✅ Scene detection: {len(scenes)} scenes found")
        
        # Test chapter splitting
        parts = generator._split_chapter_into_parts(content, 1)
        logger.info(f"✅ Chapter splitting: {len(parts)} parts")
        
        # Test key scene selection
        key_scenes = generator._select_key_scenes_for_images(scenes, target_count=2)
        logger.info(f"✅ Key scene selection: {len(key_scenes)} scenes selected")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Timeless test failed: {e}")
        return False

async def quick_test_minute_myths():
    """Quick test of Minute Myths core functionality"""
    logger.info("⚡ Quick Test: Minute Myths Core Functions")
    
    try:
        from packages.minute_myths.content_multiplier import MinuteMythsMultiplier
        
        multiplier = MinuteMythsMultiplier()
        
        # Test content template loading
        templates = multiplier._load_content_templates()
        logger.info(f"✅ Content templates: {len(templates)} types loaded")
        
        # Test character extraction
        test_story = "Perseus, son of Zeus, must slay Medusa with help from Athena and Hermes."
        characters = await multiplier._extract_characters(test_story)
        logger.info(f"✅ Character extraction: {characters}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Minute Myths test failed: {e}")
        return False

async def quick_test_dall_e_system():
    """Quick test of DALL-E system without actual generation"""
    logger.info("🎨 Quick Test: DALL-E System Readiness")
    
    try:
        from packages.core.video.ai_image_generator import AIImageGenerator
        
        generator = AIImageGenerator()
        
        # Test initialization
        if generator.openai_client:
            logger.info("✅ OpenAI client available - DALL-E ready for production")
            has_dalle = True
        else:
            logger.warning("⚠️ OpenAI client not available - need API key")
            has_dalle = False
        
        # Test stats and capabilities
        stats = generator.get_generator_stats()
        logger.info(f"✅ Generator stats: {stats['supported_pipelines']}")
        
        return has_dalle
        
    except Exception as e:
        logger.error(f"❌ DALL-E test failed: {e}")
        return False

async def run_quick_test():
    """Run quick tests of all pipeline core functions"""
    logger.info("🚀 QUICK PIPELINE CORE FUNCTIONALITY TEST")
    logger.info("="*60)
    
    results = {}
    
    # Test core functions without heavy processing
    results["timeless_core"] = await quick_test_timeless_retold()
    results["minute_myths_core"] = await quick_test_minute_myths()
    results["dalle_system"] = await quick_test_dall_e_system()
    
    # Underground API quick check
    try:
        from packages.core.api.underground_api import get_underground_api
        api = get_underground_api()
        health = api.get_system_health()
        results["underground_api"] = health.get('api_status') == 'healthy'
        logger.info(f"✅ Underground API: {health.get('api_status')}")
    except Exception as e:
        results["underground_api"] = False
        logger.error(f"❌ Underground API failed: {e}")
    
    # Summary
    logger.info("="*60)
    logger.info("🎯 QUICK TEST RESULTS")
    logger.info("="*60)
    
    total_tests = len(results)
    passed_tests = sum(1 for success in results.values() if success)
    
    for test_name, success in results.items():
        status = "✅ READY" if success else "❌ NEEDS WORK"
        test_display = test_name.replace('_', ' ').title()
        logger.info(f"   {test_display:20} {status}")
    
    logger.info("="*60)
    
    # Production readiness assessment
    core_ready = results.get("underground_api", False)
    pipelines_working = sum(1 for k, v in results.items() if k.endswith('_core') and v)
    dalle_ready = results.get("dalle_system", False)
    
    logger.info(f"Core Systems: {'✅ READY' if core_ready else '❌ NOT READY'}")
    logger.info(f"Pipeline Functions: {pipelines_working}/2 working")
    logger.info(f"DALL-E System: {'✅ READY' if dalle_ready else '⚠️ NEEDS API KEY'}")
    
    if core_ready and pipelines_working >= 2:
        if dalle_ready:
            logger.info("🎉 PRODUCTION READY! All systems operational!")
            logger.info("📈 Ready to generate and upload content across all pipelines")
        else:
            logger.info("⚠️ MOSTLY READY - Just need OpenAI API key for DALL-E 3")
            logger.info("📈 Can use existing images or add API key for full functionality")
    else:
        logger.warning("⚠️ NOT READY - Core issues need to be resolved")
    
    logger.info("="*60)
    
    return {
        "total_tests": total_tests,
        "passed_tests": passed_tests,
        "production_ready": core_ready and pipelines_working >= 2,
        "dalle_ready": dalle_ready,
        "results": results
    }

if __name__ == "__main__":
    final_results = asyncio.run(run_quick_test())