# Underground Stories - Content Storage

## 📁 Purpose
Central storage location for all generated content, assets, and output files from the three Underground Stories pipelines.

## 🏗️ Structure
```
content/
├── episode_images/        # DALL-E 3 generated images (all pipelines)
├── fairer-tales/         # Fairy tale villain POV content
│   ├── stories/          # Source story files (11 complete stories)
│   └── audio/            # Generated audio files
├── minute-myths/         # Mythology shorts content  
│   ├── audio/            # 60-second audio files
│   ├── images/           # Mobile-optimized images (9:16)
│   ├── scripts/          # Generated scripts
│   ├── videos/           # Video composition files
│   └── final_videos/     # Ready-for-upload video packages
├── timeless-retold/      # Classic literature content
│   ├── audio/            # Multi-part episode audio
│   ├── images/           # Literary scene images (16:9)
│   └── videos/           # Video composition files
├── blueprints/           # Story generation blueprints
├── youtube_ready/        # Upload-ready content with metadata
└── underground_videos/   # Final branded video packages
```

## 🔧 Role in Architecture
- **Asset Repository**: Centralized storage for all generated media
- **Pipeline Output**: Each pipeline writes to its dedicated subfolder
- **Upload Staging**: `youtube_ready/` contains production-ready content
- **Image Library**: `episode_images/` stores all DALL-E 3 generated artwork

## 📊 Content Types

### **Generated Assets**
- **Audio**: MP3 files with professional TTS narration
- **Images**: HD images from DALL-E 3 (pipeline-specific formats)
- **Scripts**: JSON and text files with story content
- **Metadata**: YouTube upload packages with titles, descriptions, tags
- **Compositions**: Remotion video configuration files

### **Source Materials**
- **Fairer Tales**: 11 complete villain POV stories
- **Classic Literature**: Full text files for Timeless Retold processing
- **Blueprints**: AI-generated story concepts and structures

## 🚀 Usage Patterns
- **Automatic Creation**: Folders created as needed during generation
- **Cross-Pipeline Sharing**: `episode_images/` used by all pipelines
- **Upload Pipeline**: Content flows from pipeline folders → `youtube_ready/`
- **Cleanup**: Old test files periodically archived

## 📏 Size Estimates
- **Images**: ~2-5MB per DALL-E 3 image  
- **Audio**: ~1MB per minute of audio content
- **Full Episode**: 15-25MB including audio, images, and metadata
- **Monthly Storage**: ~500MB-1GB for active production