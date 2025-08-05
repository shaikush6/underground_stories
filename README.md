# Underground Stories - Multi-Pipeline Content Platform

## 🎭 **Overview**
Underground Stories is a production-ready, multi-pipeline content generation platform that creates compelling audio-visual stories for automated YouTube publishing. Three distinct pipelines target different audiences with unique storytelling approaches.

## 🚀 **Quick Start**
```bash
# Launch the web interface
streamlit run web_interface/underground_stories_app.py

# Or use the run script
python3 run_underground_stories.py

# Test all systems (should show zero errors)
python3 tests/quick_pipeline_test.py
```

## 📊 **Production Status: ✅ READY**
- **All 3 Pipelines**: Fully functional with zero errors
- **DALL-E 3 Integration**: HD image generation working
- **Web Interface**: Complete user-friendly interface
- **Content Ready**: Stories, myths, and literature prepared
- **Upload Ready**: Content optimized for YouTube

## 🎬 **Content Pipelines**

### 🧚 **Fairer Tales** 
Classic fairy tales from the villain's perspective
- **Content**: 11 complete stories ready for production
- **Format**: 8-10 minute episodes split into 3 parts
- **Schedule**: Monday/Wednesday/Friday releases (11 weeks)
- **Voice**: Dramatic storytelling with OpenAI TTS

### ⚡ **Minute Myths**
Rapid-fire mythology in 60-second mobile format  
- **Content**: 1 myth → 8+ content pieces (series multiplication)
- **Format**: 9:16 vertical for TikTok/Instagram/YouTube Shorts
- **Images**: DALL-E 3 HD mobile-optimized artwork
- **Voice**: Engaging, energetic narration

### 📚 **Timeless Retold**
Classic literature adapted for modern audiences
- **Content**: Full books split into digestible episodes
- **Format**: 5-10 minute episodes with chapter splitting
- **Images**: 2-3 literary scene images with style consistency  
- **Voice**: Sophisticated literary narration

## 🏗️ **Architecture**
```
underground_stories/
├── 📦 core/              # Main application code & video generation
├── 🌐 web_interface/     # Streamlit web application  
├── 📁 content/           # Generated content & assets
├── ⚙️ config/            # API credentials & settings
├── 📊 data/              # API data storage
├── 🧪 tests/             # Test suite (zero errors expected)
├── 📚 docs/              # Complete documentation
└── 📋 logs/              # Application logs
```

## 🔧 **Setup Requirements**

### **Dependencies**
```bash
pip install -r requirements.txt  # Python packages
npm install                      # Remotion video generation
```

### **Environment (.env)**
```bash
OPENAI_API_KEY=your-openai-key                              # Required for DALL-E 3
GOOGLE_APPLICATION_CREDENTIALS=config/google-cloud-credentials.json
GOOGLE_PROJECT_ID=your-google-project-id
```

### **Configuration**
- Place API credentials in `config/` directory
- See `config/README.md` for detailed setup instructions
- YouTube integration optional but recommended

## 📖 **Documentation**
- **📋 Complete Guide**: `docs/INFO_HUB.md` - Everything you need to know
- **🔧 Setup Help**: `config/README.md` - API credentials and configuration  
- **🧪 Testing**: `tests/README.md` - How to verify everything works
- **💻 Development**: `core/README.md` - Technical architecture details

## 🎯 **Ready for Production**
✅ Zero errors across all systems  
✅ DALL-E 3 HD image generation  
✅ Professional TTS narration  
✅ Mobile and desktop optimized  
✅ Upload-ready content packages  
✅ Complete web interface  

## 🚀 **Upload Strategy**
1. **Start with Fairer Tales**: 33 videos ready, proven pipeline
2. **Launch Minute Myths**: Daily shorts for maximum engagement  
3. **Begin Timeless Retold**: Premium literary content series

---

**Status**: 🎉 **PRODUCTION READY - ALL SYSTEMS OPERATIONAL**

For detailed information, troubleshooting, and production commands, see `docs/INFO_HUB.md`.