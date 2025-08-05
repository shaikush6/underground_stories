#!/usr/bin/env python3
"""
Full Pipeline End-to-End Test
============================

Tests all 3 Underground Stories pipelines with DALL-E 3 integration
to ensure they're ready for production upload.
"""

import asyncio
import logging
from pathlib import Path
import json

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_fairer_tales_pipeline():
    """Test Fairer Tales - should already be working"""
    logger.info("🧚 Testing Fairer Tales Pipeline")
    
    try:
        # Test with existing system
        from packages.core.api.underground_api import get_underground_api
        
        api = get_underground_api()
        
        # Generate a test blueprint
        result = api.generate_blueprint("A wise owl teaches a young fox about courage")
        
        if result["success"]:
            logger.info("✅ Fairer Tales blueprint generation: SUCCESS")
            logger.info(f"   Story: {result['story_title']}")
            logger.info(f"   Genre: {result['genre']}")
            return True
        else:
            logger.error(f"❌ Fairer Tales blueprint failed: {result.get('error')}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Fairer Tales test exception: {e}")
        return False

async def test_minute_myths_pipeline():
    """Test Minute Myths with DALL-E 3 integration"""
    logger.info("⚡ Testing Minute Myths Pipeline with DALL-E 3")
    
    try:
        from packages.minute_myths.video_generator import generate_minute_myth_video
        
        # Test with Perseus myth
        result = await generate_minute_myth_video(
            myth_name="Perseus and Medusa",
            mythology_category="Greek Mythology", 
            video_format="Single Video",
            narration_style="Epic"
        )
        
        if result["success"]:
            logger.info("✅ Minute Myths generation: SUCCESS")
            logger.info(f"   Title: {result.get('video_title')}")
            logger.info(f"   Duration: {result.get('duration')} seconds")
            logger.info(f"   Mobile format: {result.get('vertical_format')}")
            logger.info(f"   Ready for upload: {result.get('ready_for_upload')}")
            return True
        else:
            logger.error(f"❌ Minute Myths generation failed: {result.get('error')}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Minute Myths test exception: {e}")
        return False

async def test_timeless_retold_pipeline():
    """Test Timeless Retold with DALL-E 3 integration"""
    logger.info("📚 Testing Timeless Retold Pipeline with DALL-E 3")
    
    try:
        # Check if we have modernized content
        test_chapter = Path("output/text/chapter_01_modernized.txt")
        if not test_chapter.exists():
            logger.warning("⚠️ No modernized content found - skipping Timeless test")
            return False
        
        from packages.timeless_retold.video_generator import generate_timeless_video
        
        result = await generate_timeless_video(
            book_title="The Lost World",
            chapter_path=str(test_chapter)
        )
        
        if result["success"]:
            logger.info("✅ Timeless Retold generation: SUCCESS")
            logger.info(f"   Title: {result.get('video_title')}")
            logger.info(f"   Duration: {result.get('duration')} minutes")
            logger.info(f"   Scenes: {result.get('scenes_count')}")
            logger.info(f"   Literary quality: {result.get('literary_quality')}")
            logger.info(f"   Ready for upload: {result.get('ready_for_upload')}")
            return True
        else:
            logger.error(f"❌ Timeless Retold generation failed: {result.get('error')}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Timeless Retold test exception: {e}")
        return False

async def test_underground_api_integration():
    """Test Underground API with all pipelines"""
    logger.info("🏗️ Testing Underground API Integration")
    
    try:
        from packages.core.api.underground_api import get_underground_api
        
        api = get_underground_api()
        
        # Test system health
        health = api.get_system_health()
        logger.info(f"   API Status: {health.get('api_status')}")
        logger.info(f"   YouTube: {health.get('youtube_api')}")
        
        # Test production status
        status = api.get_production_status()
        logger.info(f"   Current Story: {status.current_story}")
        logger.info(f"   Progress: {status.progress_percentage:.1f}%")
        logger.info(f"   YouTube Connected: {status.youtube_connected}")
        
        return health.get('api_status') == 'healthy'
        
    except Exception as e:
        logger.error(f"❌ Underground API test exception: {e}")
        return False

async def test_dalle_integration():
    """Test DALL-E 3 integration directly"""
    logger.info("🎨 Testing DALL-E 3 Integration")
    
    try:
        from packages.core.video.ai_image_generator import AIImageGenerator
        
        generator = AIImageGenerator()
        
        if not generator.openai_client:
            logger.warning("⚠️ OpenAI client not available - check API key")
            return False
        
        # Test image generation for each pipeline
        test_metadata = {
            "title": "Test Image Generation",
            "pipeline_test": True
        }
        
        test_story = "A heroic figure stands against the forces of darkness, wielding ancient power in a moment of destiny."
        
        # Test each pipeline format
        pipelines_to_test = ["fairer-tales", "timeless-retold", "minute-myths"]
        
        for pipeline in pipelines_to_test:
            try:
                logger.info(f"   Testing {pipeline} image generation...")
                
                image_path, stats = await generator.generate_episode_image(
                    story_content=test_story,
                    metadata={**test_metadata, "title": f"Test {pipeline}"},
                    pipeline=pipeline,
                    output_filename=f"test_{pipeline}.jpg"
                )
                
                logger.info(f"   ✅ {pipeline}: {stats['generation_time_seconds']:.1f}s")
                
            except Exception as e:
                logger.error(f"   ❌ {pipeline} image generation failed: {e}")
                return False
        
        logger.info("✅ DALL-E 3 integration: SUCCESS")
        return True
        
    except Exception as e:
        logger.error(f"❌ DALL-E 3 test exception: {e}")
        return False

async def run_full_pipeline_test():
    """Run comprehensive test of all pipelines for production readiness"""
    logger.info("🚀 FULL PIPELINE PRODUCTION READINESS TEST")
    logger.info("="*70)
    
    results = {}
    
    # Test 1: Underground API
    results["underground_api"] = await test_underground_api_integration()
    
    # Test 2: DALL-E 3 Integration
    results["dalle_integration"] = await test_dalle_integration()
    
    # Test 3: Fairer Tales (established pipeline)
    results["fairer_tales"] = await test_fairer_tales_pipeline()
    
    # Test 4: Minute Myths (newly integrated)
    results["minute_myths"] = await test_minute_myths_pipeline()
    
    # Test 5: Timeless Retold (newly integrated)
    results["timeless_retold"] = await test_timeless_retold_pipeline()
    
    # Final Results Summary
    logger.info("="*70)
    logger.info("🎯 PRODUCTION READINESS REPORT")
    logger.info("="*70)
    
    total_tests = len(results)
    passed_tests = sum(1 for success in results.values() if success)
    
    # Detailed results
    for test_name, success in results.items():
        status = "✅ READY" if success else "❌ NEEDS WORK"
        pipeline_name = test_name.replace('_', ' ').title()
        logger.info(f"   {pipeline_name:20} {status}")
    
    logger.info("="*70)
    
    # Upload readiness assessment
    core_systems = ["underground_api", "dalle_integration"]
    pipelines = ["fairer_tales", "minute_myths", "timeless_retold"]
    
    core_ready = all(results.get(system, False) for system in core_systems)
    pipelines_ready = [name for name in pipelines if results.get(name, False)]
    
    logger.info(f"Core Systems: {'✅ READY' if core_ready else '❌ NOT READY'}")
    logger.info(f"Ready Pipelines: {len(pipelines_ready)}/3 ({', '.join(p.replace('_', ' ').title() for p in pipelines_ready)})")
    
    if core_ready and len(pipelines_ready) >= 2:
        logger.info("🎉 PRODUCTION READY! You can start uploading content today!")
        logger.info(f"📈 Upload Strategy: Start with {len(pipelines_ready)} working pipelines")
        
        # Provide specific recommendations
        if results.get("fairer_tales"):
            logger.info("   • Fairer Tales: Continue weekly production schedule")
        if results.get("minute_myths"):
            logger.info("   • Minute Myths: Begin mythology shorts campaign")
        if results.get("timeless_retold"):
            logger.info("   • Timeless Retold: Launch classic literature series")
    else:
        logger.warning("⚠️ NOT FULLY READY - Address failed systems before production")
    
    logger.info("="*70)
    
    return {
        "total_tests": total_tests,
        "passed_tests": passed_tests,
        "production_ready": core_ready and len(pipelines_ready) >= 2,
        "ready_pipelines": pipelines_ready,
        "results": results
    }

if __name__ == "__main__":
    final_results = asyncio.run(run_full_pipeline_test())