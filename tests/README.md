# Underground Stories - Test Suite

## 📁 Purpose
Comprehensive testing framework ensuring all Underground Stories pipelines work flawlessly with zero errors.

## 🏗️ Structure
```
tests/
├── test_full_pipelines.py     # Complete end-to-end pipeline testing
├── quick_pipeline_test.py     # Fast core functionality verification  
├── test_mm_direct.py          # Minute Myths specific testing
└── test_api_methods.py        # Underground API method verification
```

## 🔧 Role in Architecture
- **Quality Assurance**: Ensures zero errors before production deployment
- **Pipeline Validation**: Tests all 3 content pipelines independently
- **API Verification**: Confirms all Underground API methods exist and function
- **Integration Testing**: End-to-end workflow validation
- **Production Readiness**: Validates systems ready for content upload

## 🧪 Test Categories

### **Pipeline Tests**
- **Fairer Tales**: Blueprint generation and story processing
- **Minute Myths**: DALL-E 3 integration and mobile video generation  
- **Timeless Retold**: Chapter processing and scene image generation
- **Cross-Pipeline**: Shared systems and API integration

### **System Tests**
- **Underground API**: All method availability and functionality
- **DALL-E 3 Integration**: Image generation across all pipelines
- **Audio Generation**: TTS processing and file creation
- **Video Composition**: Remotion integration and output files

## 🚀 Usage Commands
```bash
# Run all comprehensive tests (may take 2-3 minutes due to DALL-E generation)
python3 tests/test_full_pipelines.py

# Quick verification of core functions (30 seconds)
python3 tests/quick_pipeline_test.py

# Test specific Minute Myths functionality with real DALL-E generation
python3 tests/test_mm_direct.py

# Verify all API methods exist (instant)
python3 tests/test_api_methods.py
```

## 📊 Expected Results
- **Zero Errors**: All tests should pass with no failures
- **Production Ready**: Green status across all pipeline components
- **DALL-E Working**: Image generation successful with timing metrics
- **API Functional**: All required methods available and responsive

## ⚠️ Troubleshooting
- **DALL-E Failures**: Check `OPENAI_API_KEY` in `.env` file
- **Import Errors**: Ensure running from `underground_stories/` directory
- **Method Missing**: Restart Python to clear import cache
- **Timeout Issues**: DALL-E generation can take 30+ seconds