# Underground Stories - Complete Information Hub

## 🎭 **Project Overview**

**Underground Stories** is a multi-pipeline content generation platform for automated YouTube publishing. The platform creates compelling audio-visual stories across three distinct content pipelines, each targeting different audiences and storytelling styles.

### **Content Pipelines**

1. **🧚 Fairer Tales**: Classic fairy tales from the villain's perspective (11 stories, 8-10 min episodes)
2. **📚 Timeless Retold**: Classic literature adapted for modern audiences (5-10 min episodes with chapter splitting)
3. **⚡ Minute Myths**: Rapid-fire mythology stories in 60-second mobile format (9:16 vertical)

---

## 📊 **Current Production Status**

### ✅ **Fully Production Ready**
- **Fairer Tales Pipeline**: Complete with 11 villain POV stories
- **Minute Myths Pipeline**: DALL-E 3 integrated, mobile-optimized (1080x1920)
- **Timeless Retold Pipeline**: DALL-E 3 integrated with 2-3 images per video
- **Underground API**: All methods working, zero errors
- **Web Interface**: Full functionality for all 3 pipelines
- **DALL-E 3 Integration**: HD image generation across all pipelines

### 🔧 **Technical Architecture**

**Core Components:**
- **Web Interface**: `underground_stories/web_interface/underground_stories_app.py`
- **API Layer**: `underground_stories/core/packages/core/api/underground_api.py`
- **Pipelines**: 
  - Fairer Tales: `underground_stories/core/packages/fairer_tales/`
  - Minute Myths: `underground_stories/core/packages/minute_myths/`
  - Timeless Retold: `underground_stories/core/packages/timeless_retold/`
- **Content Storage**: `underground_stories/content/`
- **Video Generation**: `underground_stories/core/src/remotion/`

---

## 🚀 **Production Commands & Workflows**

### **Launch Underground Stories App**
```bash
cd underground_stories
python3 run_underground_stories.py
# Or run web interface directly:
streamlit run web_interface/underground_stories_app.py
```

### **Testing Commands**
```bash
# Test all pipelines (zero errors expected)
python3 tests/test_full_pipelines.py

# Quick core functionality test
python3 tests/quick_pipeline_test.py

# Test specific pipeline
python3 tests/test_mm_direct.py
```

### **Production Generation Workflow**

**Fairer Tales (Weekly Schedule):**
- 11 stories × 3 parts = 33 videos total
- Schedule: Monday/Wednesday/Friday releases for 11 weeks
- Cost: ~22¢ per 11-minute episode
- Uses OpenAI TTS with smart chunking

**Minute Myths (Daily Shorts):**
- 1 myth → 8+ content pieces (series multiplication)
- Mobile-first 9:16 format for TikTok/Instagram/YouTube Shorts
- DALL-E 3 HD images in vertical format
- 60-second episodes perfect for social media

**Timeless Retold (Literary Series):**
- Classic books split into 5-10 minute episodes
- 2-3 key scene images per video with style consistency
- Chapter splitting for proper pacing
- Premium OpenAI TTS with storytelling instructions

---

## 🎨 **Video & Visual System**

### **Image Generation (DALL-E 3)**
- **Fairer Tales**: 16:9 desktop format (1792x1024)
- **Minute Myths**: 9:16 mobile format (1024x1792)
- **Timeless Retold**: 16:9 with 2-3 images, style consistency
- **Quality**: HD generation with pipeline-specific prompts
- **Location**: `underground_stories/content/episode_images/`

### **Video Composition (Remotion)**
- **Location**: `underground_stories/core/src/remotion/`
- **Components**: Progressive reveals, text overlays, branding
- **Output**: `underground_stories/content/[pipeline]/videos/`
- **Formats**: MP4, optimized for YouTube upload

---

## 🔧 **Setup & Configuration**

### **Environment Setup**
```bash
# Required in .env file:
OPENAI_API_KEY=your-openai-key
GOOGLE_APPLICATION_CREDENTIALS=config/google-cloud-credentials.json
GOOGLE_PROJECT_ID=your-project-id
```

### **Dependencies**
```bash
pip install -r requirements.txt
npm install  # For Remotion video generation
```

### **YouTube API Setup** 
1. **Google Cloud Console**: Create "Underground Stories" project
2. **Enable APIs**: YouTube Data API v3
3. **OAuth Setup**: Configure consent screen and credentials
4. **Credentials**: Download and place in `config/youtube-credentials.json`
5. **Testing**: Use test accounts for development

### **Voice Configuration**
- **Primary TTS**: OpenAI Advanced (all pipelines)
- **Backup**: Google Chirp3-HD (Achernar voice)
- **Optimization**: Smart chunking, concatenation, storytelling instructions
- **Cost**: ~$3-5/month for full production

---

## 📁 **Project Structure**

```
underground_stories/
├── core/
│   ├── packages/          # Main application code
│   └── src/remotion/      # Video generation components
├── web_interface/         # Streamlit web app
├── content/               # Generated content & assets
├── config/                # Configuration files
├── data/                  # API data storage
├── tests/                 # Test files
├── docs/                  # Documentation
└── logs/                  # Application logs
```

---

## 🎯 **Ready for Upload - Production Checklist**

### ✅ **Technical Readiness**
- [x] All 3 pipelines tested with zero errors
- [x] DALL-E 3 integration working across all pipelines
- [x] Underground API methods all functional
- [x] Web interface fully operational
- [x] Content generation working end-to-end

### ✅ **Content Readiness**
- [x] **Fairer Tales**: 11 complete stories ready for 33-video series
- [x] **Minute Myths**: Content multiplication system (1 myth → 8+ videos)
- [x] **Timeless Retold**: Chapter processing with proper episode splitting

### 🚀 **Upload Strategy**
1. **Start with Fairer Tales**: Established pipeline, weekly schedule
2. **Launch Minute Myths**: Daily shorts for maximum engagement
3. **Begin Timeless Retold**: Premium literary content series

---

## 🔍 **Troubleshooting**

### **Common Issues**
1. **DALL-E Not Working**: Check `.env` file has `OPENAI_API_KEY`
2. **Import Errors**: Ensure you're running from correct directory
3. **Path Issues**: All paths should be absolute, check Path objects
4. **API Method Missing**: Restart Python completely to clear cache

### **Debug Commands**
```bash
# Test DALL-E integration
python3 tests/test_mm_direct.py

# Check API methods
python3 tests/test_api_methods.py

# Full system health check
python3 tests/quick_pipeline_test.py
```

---

## 📈 **Future Enhancements**

### **Planned Features**
- YouTube auto-uploading integration
- Weekly scheduler automation  
- Analytics dashboard
- Multi-language support
- Advanced voice cloning

### **Expansion Possibilities**
- Podcast distribution (Spotify, Apple Podcasts)
- International mythology for Minute Myths
- Additional literary genres for Timeless Retold
- Interactive story elements

---

**Status**: ✅ **PRODUCTION READY - ALL SYSTEMS OPERATIONAL**

Last Updated: August 2025