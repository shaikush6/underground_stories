# Underground Stories - Core Components

## 📁 Purpose
Contains the core application code and video generation components for Underground Stories.

## 🏗️ Structure
```
core/
├── packages/           # Main application packages
│   ├── core/          # Shared core functionality (API, audio, video)
│   ├── fairer_tales/  # Fairy tale villain POV pipeline  
│   ├── minute_myths/  # 60-second mythology shorts pipeline
│   └── timeless_retold/ # Classic literature adaptation pipeline
└── src/remotion/      # Video composition and generation components
```

## 🔧 Role in Architecture
- **API Layer**: Central Underground Stories API (`packages/core/api/`)
- **Audio Pipeline**: TTS integration and audio processing (`packages/core/audio/`)
- **Video Generation**: DALL-E 3 image generation (`packages/core/video/`)
- **Content Pipelines**: Three distinct content generation systems
- **Remotion Integration**: React-based video composition for final output

## 🚀 Key Files
- `packages/core/api/underground_api.py` - Main API with all pipeline methods
- `packages/core/video/ai_image_generator.py` - DALL-E 3 integration
- `packages/*/video_generator.py` - Pipeline-specific video generation
- `src/remotion/components/` - Video composition React components

## 🔗 Dependencies
- Requires `.env` with OpenAI API key for DALL-E 3
- Needs `requirements.txt` packages installed
- Uses Remotion for video rendering (requires npm install)