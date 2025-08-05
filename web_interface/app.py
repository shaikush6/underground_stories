#!/usr/bin/env python3
"""
The Flipside Web App
===================

Streamlit web interface for generating stories from blueprints.
"""

import streamlit as st
import sys
import os
from pathlib import Path
import json
from datetime import datetime
import time

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from story_blueprint_processor import FlipsideProcessor
from modernization_config import POV_STYLES

# Import Underground Stories components
try:
    from packages.core.api.underground_api import get_underground_api
    UNDERGROUND_AVAILABLE = True
except ImportError:
    UNDERGROUND_AVAILABLE = False
    print("⚠️ Underground Stories API not available")

# Page config - Updated for Underground Stories
st.set_page_config(
    page_title="Underground Stories Platform",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Underground Stories Theme
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(45deg, #B87333, #00BFFF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .story-card {
        background: #2C2C2C;
        color: #F5F5F5;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #B87333;
        margin: 1rem 0;
    }
    .blueprint-example {
        background: #2C2C2C;
        color: #F5F5F5;
        padding: 1rem;
        border-radius: 5px;
        font-family: monospace;
        font-size: 0.9rem;
        border: 1px solid #B87333;
    }
    .underground-stats {
        background: #2C2C2C;
        color: #F5F5F5;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #00BFFF;
        margin: 0.5rem 0;
    }
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
    }
    .status-active { background-color: #00BFFF; }
    .status-warning { background-color: #B87333; }
    .status-error { background-color: #FF4444; }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">🎬 Underground Stories Platform</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #B87333;">Complete content creation pipeline from blueprints to YouTube</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Style selection
        style_options = list(POV_STYLES.keys())
        selected_style = st.selectbox(
            "Story Style",
            style_options,
            index=0,
            help="Choose the narrative tone and approach"
        )
        
        # Show style description
        if selected_style in POV_STYLES:
            style_info = POV_STYLES[selected_style]
            st.info(f"**{style_info['description']}**\n\nTone: {style_info['tone']}")
        
        st.markdown("---")
        
        # Quick links
        st.header("📚 Resources")
        st.markdown("- [Blueprint Format Guide](#blueprint-format)")
        st.markdown("- [Example Stories](#examples)")
        st.markdown("- [Export Options](#export)")
    
    # Main content tabs - Underground Stories Platform
    if UNDERGROUND_AVAILABLE:
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📝 Generate Story", 
            "🎨 Blueprint Generator", 
            "📊 Production Dashboard",
            "🎬 Video Production",
            "📋 Format Guide", 
            "📖 Examples"
        ])
    else:
        tab1, tab2, tab3 = st.tabs(["📝 Generate Story", "📋 Blueprint Format", "📖 Example Stories"])
    
    with tab1:
        generate_story_tab(selected_style)
    
    if UNDERGROUND_AVAILABLE:
        with tab2:
            blueprint_generator_tab()
        
        with tab3:
            production_dashboard_tab()
        
        with tab4:
            video_production_tab()
        
        with tab5:
            blueprint_format_tab()
        
        with tab6:
            example_stories_tab()
    else:
        with tab2:
            blueprint_format_tab()
        
        with tab3:
            example_stories_tab()

def generate_story_tab(selected_style):
    st.header("Generate Your Story")
    
    # Blueprint input
    st.subheader("Story Blueprint")
    blueprint_text = st.text_area(
        "Paste your story blueprint here:",
        height=400,
        placeholder="""17 Green Card — Dark Fantasy / Witness-Protection Parable

Logline: A wetlands witch disguises endangered whistle-blowers as frogs; when a reality-TV princess kisses one on camera, the entire safe-house network is exposed to royal assassins.

| Character | Mirella ("Bog Witch"), shapeshift specialist |
| Conflict  | Preserve network vs. viral "fairy-tale rescue" spectacle |
| Setting   | Haunted marsh with lily-pad portals to exile realms |
| Theme     | Bodily autonomy, voyeuristic saviorism, asylum politics |

Arc
    1.    Exposition: Mirella escorts new client—Prince Corvin, palace corruption witness—into frog form.
    2.    Inciting: Princess Liora launches "Frog-Prince Quest" reality show, crowdsourcing kisses.
    3.    Rising: Producers home in on Mirella's marsh; drones film frogs; Liora kisses Corvin, partial re-humanization broadcast live.
    4.    Climax: Assassin squad arrives; Mirella unleashes swamp spirits, re-frogifies Liora to stall feed, evacuates clients through mud-portal.
    5.    Falling: Media spins story as terrorist witchcraft; monarchy denies hit squad.
    6.    Resolution: International tribunal grants frogs (now human) political asylum; Mirella vanishes into deeper bog, new portal glowing."""
    )
    
    # Generate button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Generate Story", type="primary", use_container_width=True):
            if blueprint_text.strip():
                generate_story(blueprint_text, selected_style)
            else:
                st.error("Please enter a story blueprint first!")

def generate_story(blueprint_text, style):
    """Generate story from blueprint"""
    with st.spinner("🎭 Generating your story..."):
        try:
            # Initialize processor
            if 'processor' not in st.session_state:
                st.session_state.processor = FlipsideProcessor()
            
            # Process blueprint
            result = st.session_state.processor.process_blueprint_text(blueprint_text, style)
            
            if result['success']:
                st.success(f"✅ Story generated: **{result['story_title']}**")
                st.info(f"📊 Word count: {result['word_count']} | Style: {result['style']}")
                
                # Read and display the generated story
                with open(result['filepath'], 'r', encoding='utf-8') as f:
                    story_content = f.read()
                
                # Display story
                st.markdown("---")
                st.header("📖 Your Generated Story")
                
                # Story content in a nice container
                with st.container():
                    st.markdown(f'<div class="story-card">{story_content}</div>', unsafe_allow_html=True)
                
                # Download button
                st.download_button(
                    label="📥 Download Story",
                    data=story_content,
                    file_name=f"{result['story_title'].replace(' ', '_').lower()}.txt",
                    mime="text/plain"
                )
                
                # Save to session state for potential editing
                st.session_state.last_generated_story = {
                    'content': story_content,
                    'title': result['story_title'],
                    'filepath': result['filepath']
                }
                
            else:
                st.error(f"❌ Error generating story: {result['error']}")
                
        except Exception as e:
            st.error(f"❌ Unexpected error: {str(e)}")

def blueprint_format_tab():
    st.header("Blueprint Format Guide")
    
    st.markdown("""
    ### Required Format Structure
    
    Your blueprint should follow this exact format:
    """)
    
    format_example = """[ID] [Title] — [Genre/Style]

Logline: [One sentence describing the core concept and hook]

| Character | [Main character description] |
| Conflict  | [Central conflict description] |
| Setting   | [Where the story takes place] |
| Theme     | [Main themes to explore] |

Arc
    1.    Exposition: [Opening situation]
    2.    Inciting: [Inciting incident that starts the story]
    3.    Rising: [Rising action and complications]
    4.    Climax: [Major confrontation or turning point]
    5.    Falling: [Consequences and falling action]
    6.    Resolution: [How the story concludes]"""
    
    st.markdown(f'<div class="blueprint-example">{format_example}</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ### Tips for Great Blueprints
    
    - **Strong Logline**: Make it hook the reader in one sentence
    - **Complex Character**: Give your villain depth and sympathetic motivations
    - **Clear Conflict**: What does your protagonist want vs. what stands in their way?
    - **Vivid Setting**: Create a world that supports your themes
    - **Meaningful Themes**: What social issues or human truths are you exploring?
    - **Tight Arc**: Each story beat should escalate tension and develop character
    """)

def example_stories_tab():
    st.header("Example Story Blueprints")
    
    examples = [
        {
            "title": "Green Card (Frog Prince)",
            "blueprint": """17 Green Card — Dark Fantasy / Witness-Protection Parable

Logline: A wetlands witch disguises endangered whistle-blowers as frogs; when a reality-TV princess kisses one on camera, the entire safe-house network is exposed to royal assassins.

| Character | Mirella ("Bog Witch"), shapeshift specialist |
| Conflict  | Preserve network vs. viral "fairy-tale rescue" spectacle |
| Setting   | Haunted marsh with lily-pad portals to exile realms |
| Theme     | Bodily autonomy, voyeuristic saviorism, asylum politics |

Arc
    1.    Exposition: Mirella escorts new client—Prince Corvin, palace corruption witness—into frog form.
    2.    Inciting: Princess Liora launches "Frog-Prince Quest" reality show, crowdsourcing kisses.
    3.    Rising: Producers home in on Mirella's marsh; drones film frogs; Liora kisses Corvin, partial re-humanization broadcast live.
    4.    Climax: Assassin squad arrives; Mirella unleashes swamp spirits, re-frogifies Liora to stall feed, evacuates clients through mud-portal.
    5.    Falling: Media spins story as terrorist witchcraft; monarchy denies hit squad.
    6.    Resolution: International tribunal grants frogs (now human) political asylum; Mirella vanishes into deeper bog, new portal glowing."""
        },
        {
            "title": "The Forest Therapist (Red Riding Hood)",
            "blueprint": """01 The Forest Therapist — Psychological Drama / Environmental Thriller

Logline: An eco-therapist wolf helps traumatized forest animals heal, but when a poacher's daughter starts using his sanctuary as a delivery route, his patients' safety is threatened.

| Character | Dr. Fenris Wolf, wildlife psychologist and forest guardian |
| Conflict  | Protect animal sanctuary vs. human encroachment and illegal activities |
| Setting   | Ancient forest preserve with hidden therapy clearings and safe spaces |
| Theme     | Environmental destruction, trauma healing, the cost of sanctuary |

Arc
    1.    Exposition: Dr. Wolf conducts therapy session with PTSD deer; establishes his sanctuary work.
    2.    Inciting: Red (Ruby) starts cutting through forest to deliver mysterious packages to "Grandmother."
    3.    Rising: Wolf discovers packages contain animal fighting equipment; Ruby's routes disturb traumatized animals.
    4.    Climax: Wolf confronts Ruby during delivery, reveals Grandmother's illegal animal fighting ring.
    5.    Falling: Ruby must choose between family loyalty and doing what's right; authorities investigate.
    6.    Resolution: Ruby becomes Wolf's ally, helps relocate animals; sanctuary expands with new protection."""
        }
    ]
    
    for i, example in enumerate(examples):
        with st.expander(f"📝 {example['title']}"):
            st.markdown(f'<div class="blueprint-example">{example["blueprint"]}</div>', unsafe_allow_html=True)
            
            if st.button(f"Try This Example", key=f"example_{i}"):
                # Copy to clipboard (simulation)
                st.info("💡 Copy the blueprint above and paste it into the Generate Story tab!")

def blueprint_generator_tab():
    """Underground Stories Blueprint Generator Tab"""
    st.header("🎨 Blueprint Generator")
    
    if not UNDERGROUND_AVAILABLE:
        st.error("Underground Stories API not available")
        return
    
    try:
        api = get_underground_api()
        
        st.markdown("""
        Generate detailed story blueprints from simple concepts using our expansion methodology.
        Perfect for creating rich foundations for Underground Stories.
        """)
        
        # Input section
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("📝 Story Concept")
            story_concept = st.text_input(
                "Enter your story concept or title:",
                placeholder="e.g., Huff & Heal, High Crimes, Sugar Shelter"
            )
            
            base_fairy_tale = st.text_input(
                "Base fairy tale (optional):",
                placeholder="e.g., Little Red Riding Hood, Jack and the Beanstalk"
            )
        
        with col2:
            st.subheader("🎯 Available Blueprints")
            available_blueprints = api.get_available_blueprints()
            
            if available_blueprints:
                for blueprint in available_blueprints[:5]:  # Show first 5
                    st.markdown(f"**{blueprint['title']}** - {blueprint['genre']}")
            else:
                st.info("No blueprints generated yet")
        
        # Generate button
        if st.button("🎨 Generate Blueprint", type="primary"):
            if story_concept.strip():
                with st.spinner("🎨 Generating detailed blueprint..."):
                    result = api.generate_blueprint(story_concept, base_fairy_tale)
                
                if result['success']:
                    st.success(f"✅ Blueprint generated: **{result['story_title']}**")
                    
                    # Display blueprint
                    st.subheader("📋 Generated Blueprint")
                    
                    with st.expander("🔍 View Full Blueprint", expanded=True):
                        blueprint_data = result['blueprint']
                        
                        # Original story section
                        st.markdown("### Original Story Analysis")
                        orig = blueprint_data['original']
                        st.markdown(f"**Title:** {orig['title']}")
                        st.markdown(f"**Genre:** {orig['genre']}")
                        st.markdown(f"**Theme:** {orig['theme']}")
                        
                        # New story section
                        st.markdown("### New Story Blueprint")
                        new = blueprint_data['new']
                        st.markdown(f"**Title:** {new['title']}")
                        st.markdown(f"**Genre:** {new['genre']}")
                        st.markdown(f"**Logline:** {new['logline']}")
                        
                        # Components table
                        components_data = [
                            ["Character", new['character']['expanded_description'][:150] + "..."],
                            ["Conflict", new['conflict']['expanded_description'][:150] + "..."],
                            ["Setting", new['setting']['expanded_description'][:150] + "..."],
                            ["Theme", new['theme']['expanded_description'][:150] + "..."]
                        ]
                        
                        import pandas as pd
                        df = pd.DataFrame(components_data, columns=["Component", "Description"])
                        st.table(df)
                    
                    # Export options
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Download as JSON
                        blueprint_json = json.dumps(result['blueprint'], indent=2)
                        st.download_button(
                            "📥 Download Blueprint (JSON)",
                            blueprint_json,
                            f"{result['story_title']}_blueprint.json",
                            "application/json"
                        )
                    
                    with col2:
                        # Download Flipside format
                        st.download_button(
                            "📥 Download Flipside Format",
                            result['flipside_format'],
                            f"{result['story_title']}_flipside.txt",
                            "text/plain"
                        )
                
                else:
                    st.error(f"❌ Blueprint generation failed: {result['error']}")
            else:
                st.error("Please enter a story concept!")
                
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

def production_dashboard_tab():
    """Underground Stories Production Dashboard"""
    st.header("📊 Production Dashboard")
    
    if not UNDERGROUND_AVAILABLE:
        st.error("Underground Stories API not available")
        return
    
    try:
        api = get_underground_api()
        
        # System health check
        health = api.get_system_health()
        production_status = api.get_production_status()
        
        # Status indicators
        st.subheader("🏥 System Health")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            api_status = "active" if health['api_status'] == "healthy" else "error"
            st.markdown(f"""
            <div class="underground-stats">
                <span class="status-indicator status-{api_status}"></span>
                <strong>API Status</strong><br>
                {health['api_status'].title()}
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            youtube_status = "active" if health['youtube_api'] == "connected" else "warning"
            st.markdown(f"""
            <div class="underground-stats">
                <span class="status-indicator status-{youtube_status}"></span>
                <strong>YouTube API</strong><br>
                {health['youtube_api'].title()}
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            scheduler_status = "active" if health['scheduler'] == "available" else "error"
            st.markdown(f"""
            <div class="underground-stats">
                <span class="status-indicator status-{scheduler_status}"></span>
                <strong>Scheduler</strong><br>
                {health['scheduler'].title()}
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            blueprint_status = "active" if health['blueprint_generator'] == "available" else "error"
            st.markdown(f"""
            <div class="underground-stats">
                <span class="status-indicator status-{blueprint_status}"></span>
                <strong>Blueprint Gen</strong><br>
                {health['blueprint_generator'].title()}
            </div>
            """, unsafe_allow_html=True)
        
        # Production status
        st.subheader("🎬 Production Status")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Progress bar
            progress = production_status.progress_percentage / 100
            st.progress(progress)
            st.markdown(f"**Progress:** {production_status.progress_percentage:.1f}% ({production_status.current_week}/{production_status.total_stories})")
            
            # Current story
            st.markdown(f"**Current Story:** {production_status.current_story}")
            st.markdown(f"**Next Scheduled Run:** {production_status.next_scheduled_run}")
            
            if production_status.last_generation:
                st.markdown(f"**Last Generation:** {production_status.last_generation}")
        
        with col2:
            # Quick stats
            st.markdown(f"""
            <div class="underground-stats">
                <strong>Completed Stories</strong><br>
                {len(production_status.completed_stories)}
            </div>
            """, unsafe_allow_html=True)
            
            if production_status.failed_stories:
                st.markdown(f"""
                <div class="underground-stats">
                    <strong>Failed Stories</strong><br>
                    {len(production_status.failed_stories)}
                </div>
                """, unsafe_allow_html=True)
        
        # Content pipelines
        st.subheader("📺 Content Pipelines")
        
        pipelines = ["fairer-tales", "timeless-retold", "minute-myths"]
        
        for pipeline in pipelines:
            pipeline_status = api.get_pipeline_status(pipeline)
            
            if 'error' not in pipeline_status:
                status_color = "active" if pipeline_status['status'] == "active" else "warning"
                
                with st.expander(f"📊 {pipeline_status['pipeline'].title()} Pipeline"):
                    st.markdown(f"""
                    **Status:** <span class="status-indicator status-{status_color}"></span>{pipeline_status['status'].title()}
                    """, unsafe_allow_html=True)
                    
                    if pipeline == "fairer-tales":
                        st.markdown(f"**Progress:** {pipeline_status['progress']:.1f}%")
                        st.markdown(f"**Completed:** {len(pipeline_status['completed'])}")
                        st.markdown(f"**Next Run:** {pipeline_status['next_run']}")
                    else:
                        st.markdown(f"**Description:** {pipeline_status['description']}")
                        st.markdown(f"**Stage:** {pipeline_status['implementation_stage']}")
                        
                        if 'features' in pipeline_status:
                            st.markdown("**Features:**")
                            for feature in pipeline_status['features']:
                                st.markdown(f"• {feature}")
        
        # Manual controls
        st.subheader("🔧 Manual Controls")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🚀 Run Manual Production", type="primary"):
                with st.spinner("Running manual production..."):
                    result = api.trigger_manual_production()
                
                if result['success']:
                    st.success("✅ Manual production completed!")
                    st.rerun()
                else:
                    st.error(f"❌ Manual production failed: {result['error']}")
        
        with col2:
            if st.button("🔄 Refresh Status"):
                st.rerun()
        
        with col3:
            if st.button("📊 Test YouTube Connection"):
                with st.spinner("Testing YouTube connection..."):
                    result = api.test_youtube_connection()
                
                if result['connected']:
                    st.success(f"✅ Connected to: {result.get('channel_info', {}).get('title', 'YouTube')}")
                else:
                    st.error(f"❌ Connection failed: {result['error']}")
                    
    except Exception as e:
        st.error(f"❌ Dashboard error: {str(e)}")

def video_production_tab():
    """Video Production Testing Tab"""
    st.header("🎬 Video Production")
    
    if not UNDERGROUND_AVAILABLE:
        st.error("Underground Stories API not available")
        return
    
    try:
        api = get_underground_api()
        
        st.markdown("""
        Test video generation and YouTube upload functionality.
        Generate single videos for testing before full production runs.
        """)
        
        # Video generation section
        st.subheader("🎥 Generate Test Video")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            story_title = st.text_input(
                "Story Title:",
                value="Huff & Heal",
                placeholder="Enter story title for video generation"
            )
            
            part_number = st.number_input(
                "Part Number:",
                min_value=1,
                max_value=3,
                value=1
            )
        
        with col2:
            st.info("""
            **Video Test Info:**
            • Generates single video part
            • Uses existing audio files
            • Creates test output
            • Validates pipeline
            """)
        
        if st.button("🎬 Generate Test Video", type="primary"):
            if story_title:
                with st.spinner(f"Generating video for {story_title} Part {part_number}..."):
                    result = api.generate_single_story_video(story_title, part_number)
                
                if result.success:
                    st.success(f"✅ Video generated successfully!")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"**File:** {result.video_path}")
                        st.markdown(f"**Size:** {result.file_size_mb}MB")
                    
                    with col2:
                        st.markdown(f"**Generated:** {result.generation_time}")
                        
                        if result.duration_seconds:
                            st.markdown(f"**Duration:** {result.duration_seconds}s")
                    
                    # Store for potential upload
                    st.session_state.last_generated_video = {
                        'path': result.video_path,
                        'title': f"{story_title} - Part {part_number}",
                        'story_title': story_title,
                        'part': part_number
                    }
                
                else:
                    st.error(f"❌ Video generation failed: {result.error}")
            else:
                st.error("Please enter a story title!")
        
        # YouTube upload section
        st.subheader("📤 YouTube Upload Test")
        
        if 'last_generated_video' in st.session_state:
            video_info = st.session_state.last_generated_video
            
            st.info(f"**Ready to upload:** {video_info['title']}")
            
            # Upload configuration
            upload_title = st.text_input(
                "YouTube Title:",
                value=f"Underground Stories: {video_info['title']} [TEST]"
            )
            
            upload_description = st.text_area(
                "Description:",
                value=f"""Underground Stories presents: {video_info['story_title']}
                
This is a test upload from our automated production system.
                
#UndergroundStories #FairerTales #ModernFairyTales""",
                height=150
            )
            
            tags = st.text_input(
                "Tags (comma-separated):",
                value="underground stories, fairy tales, modern retelling, audio drama"
            )
            
            privacy_status = st.selectbox(
                "Privacy Status:",
                ["private", "unlisted", "public"],
                index=0
            )
            
            if st.button("📤 Upload to YouTube", type="secondary"):
                if upload_title and upload_description:
                    with st.spinner("Uploading to YouTube..."):
                        tag_list = [tag.strip() for tag in tags.split(",") if tag.strip()]
                        
                        result = api.upload_video_to_youtube(
                            video_path=video_info['path'],
                            title=upload_title,
                            description=upload_description,
                            tags=tag_list,
                            privacy_status=privacy_status
                        )
                    
                    if result.success:
                        st.success("✅ Video uploaded successfully!")
                        st.markdown(f"**Video ID:** {result.video_id}")
                        st.markdown(f"**URL:** [Watch on YouTube]({result.video_url})")
                        
                        if result.scheduled_time:
                            st.markdown(f"**Scheduled for:** {result.scheduled_time}")
                    
                    else:
                        st.error(f"❌ Upload failed: {result.error}")
                else:
                    st.error("Please fill in title and description!")
        else:
            st.info("Generate a test video first to enable YouTube upload testing.")
            
    except Exception as e:
        st.error(f"❌ Video production error: {str(e)}")

if __name__ == "__main__":
    main()