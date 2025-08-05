# Underground Stories - Web Interface

## 📁 Purpose
Streamlit-based web application providing user-friendly interface for all Underground Stories content generation pipelines.

## 🏗️ Structure
```
web_interface/
├── underground_stories_app.py    # Main Streamlit application
└── app.py                       # Alternative entry point
```

## 🔧 Role in Architecture
- **User Interface**: Primary way users interact with Underground Stories
- **Pipeline Control**: Unified interface for all 3 content pipelines
- **Real-time Generation**: Live content creation with progress feedback
- **Content Management**: Browse and manage generated content

## 🎯 Features
- **Fairer Tales**: Generate villain POV fairy tale episodes
- **Minute Myths**: Create 60-second mythology shorts with mobile optimization
- **Timeless Retold**: Process classic literature into modern episodes
- **DALL-E 3 Integration**: HD image generation across all pipelines
- **Content Preview**: View generated scripts, audio, and video compositions

## 🚀 How to Use
```bash
# Launch from underground_stories directory
streamlit run web_interface/underground_stories_app.py

# Or use the run script
python3 run_underground_stories.py
```

## 📊 Interface Sections
1. **Pipeline Selection**: Choose between 3 content types
2. **Content Input**: Story details, myth names, or book chapters  
3. **Generation Control**: Start/stop content creation process
4. **Results Display**: Preview generated content and download files
5. **System Status**: Monitor API health and generation progress

## 🔗 Dependencies
- Streamlit framework for web interface  
- Underground Stories API for backend functionality
- All core packages must be installed and functional