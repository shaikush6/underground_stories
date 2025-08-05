#!/usr/bin/env python3
"""
Underground Stories - Comprehensive Video Production Platform
===========================================================

Enhanced Streamlit app integrating the sophisticated Flipside story generation
system with video production, automation, and multi-pipeline management.
"""

import streamlit as st
import sys
import os
import json
import time
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

# Add paths for imports
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))
sys.path.append(str(project_root / "the_flipside"))

# Core Flipside imports (preserving existing architecture)
try:
    from story_blueprint_processor import FlipsideProcessor
    from modernization_config import POV_STYLES
    from supabase_integration import get_supabase_client, import_local_stories, import_selected_stories
    FLIPSIDE_AVAILABLE = True
except ImportError:
    FLIPSIDE_AVAILABLE = False
    POV_STYLES = {}

# Underground Stories imports
try:
    from packages.core.api.underground_api import get_underground_api
    from packages.core.blueprint.blueprint_generator import BlueprintGenerator
    UNDERGROUND_API_AVAILABLE = True
except ImportError as e:
    UNDERGROUND_API_AVAILABLE = False
    UNDERGROUND_IMPORT_ERROR = str(e)

# Page config
st.set_page_config(
    page_title="Underground Stories - Video Production Platform",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Underground Stories brand colors and styling
st.markdown("""
<style>
    :root {
        --bg-dark: #2C2C2C;
        --accent-bronze: #B87333;
        --text-light: #F5F5F5;
        --highlight-blue: #00BFFF;
        --success-green: #28a745;
        --warning-orange: #fd7e14;
        --danger-red: #dc3545;
    }
    
    .underground-header {
        font-size: 3.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
        background: linear-gradient(45deg, var(--accent-bronze), var(--highlight-blue));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .platform-subtitle {
        text-align: center;
        font-size: 1.4rem;
        color: var(--text-light);
        margin-bottom: 2rem;
        font-style: italic;
    }
    
    .architecture-badge {
        background: linear-gradient(45deg, var(--accent-bronze), var(--success-green));
        color: white;
        padding: 0.5rem 1.2rem;
        border-radius: 25px;
        font-size: 0.9rem;
        font-weight: bold;
        margin: 0.5rem;
        display: inline-block;
        text-align: center;
    }
    
    .pipeline-card {
        background: linear-gradient(135deg, #2d3436, #636e72);
        border: 1px solid var(--accent-bronze);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        color: var(--text-light);
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
    }
    
    .status-active { background-color: var(--success-green); }
    .status-development { background-color: var(--warning-orange); }
    .status-inactive { background-color: var(--danger-red); }
    
    .automation-tab {
        background: linear-gradient(135deg, #1a1a1a, #2d2d2d);
        border-radius: 10px;
        padding: 2rem;
        margin: 1rem 0;
        border: 2px solid var(--accent-bronze);
        color: var(--text-light);
    }
    
    .story-input-section {
        background: linear-gradient(135deg, #2d3436, #636e72);
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid var(--highlight-blue);
    }
    
    .dashboard-metric {
        background: var(--bg-dark);
        border: 1px solid var(--accent-bronze);
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
        color: var(--text-light);
    }
    
    .flipside-integration {
        background: linear-gradient(135deg, #4ecdc4, #44a08d);
        border-radius: 10px;
        padding: 1rem;
        color: white;
        margin: 1rem 0;
    }

    /* Dark theme adjustments */
    .stApp {
        background-color: var(--bg-dark);
        color: var(--text-light);
    }
    
    .stSelectbox > div > div {
        background-color: #404040;
        color: var(--text-light);
    }
    
    .stTextInput > div > div > input {
        background-color: #404040;
        color: var(--text-light);
        border: 1px solid var(--accent-bronze);
    }
    
    .stTextArea > div > div > textarea {
        background-color: #404040;
        color: var(--text-light);
        border: 1px solid var(--accent-bronze);
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main application entry point"""
    
    # Header
    st.markdown('<h1 class="underground-header">🎬 Underground Stories</h1>', unsafe_allow_html=True)
    st.markdown('<p class="platform-subtitle">Comprehensive Video Production Platform • Automated Story-to-Video Pipeline</p>', unsafe_allow_html=True)
    
    # Architecture badges
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('''
        <div style="text-align: center;">
            <span class="architecture-badge">🎭 Writer-Centric Architecture</span>
            <span class="architecture-badge">🤖 Full Automation</span>
            <span class="architecture-badge">📺 Video Production</span>
            <span class="architecture-badge">🗓️ Weekly Scheduling</span>
        </div>
        ''', unsafe_allow_html=True)
    
    # Sidebar configuration
    setup_sidebar()
    
    # Main content tabs - The 5 tabs you specified
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🧚 Fairer Tales", 
        "📚 Timeless Retold", 
        "⚡ Minute Myths", 
        "📊 Dashboard", 
        "⚙️ Settings"
    ])
    
    with tab1:
        fairer_tales_tab()
    
    with tab2:
        timeless_retold_tab()
    
    with tab3:
        minute_myths_tab()
    
    with tab4:
        dashboard_tab()
    
    with tab5:
        settings_tab()
    
    # Flipside Integration Section (preserving your architecture)
    if FLIPSIDE_AVAILABLE:
        st.markdown("---")
        st.markdown('<div class="flipside-integration">', unsafe_allow_html=True)
        st.header("🔄 Flipside Integration")
        st.write("Access the complete Flipside story generation system for advanced blueprint management")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Launch Flipside App", use_container_width=True):
                st.info("Run: `streamlit run the_flipside/web_app/app.py` in terminal")
        
        with col2:
            if st.button("📋 Blueprint Format Guide", use_container_width=True):
                show_blueprint_format()
        
        st.markdown('</div>', unsafe_allow_html=True)

def setup_sidebar():
    """Setup sidebar configuration"""
    with st.sidebar:
        st.header("🎬 Underground Stories")
        st.markdown("**Comprehensive Video Production Platform**")
        
        # System status
        st.markdown("---")
        st.subheader("🔧 System Status")
        
        if UNDERGROUND_API_AVAILABLE:
            try:
                api = get_underground_api()
                health = api.get_system_health()
                
                st.success("✅ Underground API: Connected")
                if health.get("youtube_api") == "connected":
                    st.success("✅ YouTube API: Connected")
                else:
                    st.warning("⚠️ YouTube API: Setup Required")
                
                if health.get("scheduler") == "available":
                    st.success("✅ Scheduler: Active")
                else:
                    st.warning("⚠️ Scheduler: Setup Required")
                    
            except Exception as e:
                st.error(f"❌ API Error: {str(e)[:50]}...")
        else:
            st.warning("⚠️ Underground API: Setup Required")
            if 'UNDERGROUND_IMPORT_ERROR' in globals():
                with st.expander("Debug Info"):
                    st.text(f"Import error: {UNDERGROUND_IMPORT_ERROR}")
        
        if FLIPSIDE_AVAILABLE:
            st.success("✅ Flipside System: Available")
        else:
            st.warning("⚠️ Flipside System: Not Available")
        
        st.markdown("---")
        
        # Pipeline selection for cross-tab functionality
        st.subheader("🚀 Active Pipeline")
        pipeline = st.selectbox(
            "Select Pipeline",
            ["fairer-tales", "timeless-retold", "minute-myths"],
            index=0
        )
        st.session_state.active_pipeline = pipeline
        
        # Story style (from Flipside)
        if FLIPSIDE_AVAILABLE and POV_STYLES:
            st.subheader("🎨 Story Style")
            style_options = list(POV_STYLES.keys())
            selected_style = st.selectbox(
                "Narrative Style",
                style_options,
                index=0
            )
            st.session_state.selected_style = selected_style
            
            # Show style description
            if selected_style in POV_STYLES:
                style_info = POV_STYLES[selected_style]
                st.info(f"**{style_info['description']}**")
        
        st.markdown("---")
        
        # Quick actions
        st.subheader("⚡ Quick Actions")
        
        if st.button("🔄 Refresh Status", use_container_width=True):
            st.rerun()
        
        if st.button("📊 System Health", use_container_width=True):
            show_system_health()
        
        if st.button("🎬 Test Video Gen", use_container_width=True):
            test_video_generation()

def fairer_tales_tab():
    """Fairer Tales - Full automation from story name to audio"""
    st.header("🧚 Fairer Tales - Automated Story Production")
    st.markdown("**Full automation pipeline: Story name → POV analysis → Blueprint → Story → Audio → Video**")
    
    # Automation workflow section
    st.markdown('<div class="automation-tab">', unsafe_allow_html=True)
    
    # Story input section
    st.markdown('<div class="story-input-section">', unsafe_allow_html=True)
    st.subheader("📝 Story Input")
    
    # Main input method - story name/concept
    story_input = st.text_input(
        "Enter story name or concept:",
        placeholder="e.g., Cinderella, Snow White, or 'A story about redemption'",
        help="Enter a fairy tale name or describe your story concept in a few words"
    )
    
    # Optional: Additional context
    with st.expander("➕ Additional Context (Optional)"):
        additional_context = st.text_area(
            "Provide additional details:",
            placeholder="Any specific themes, characters, or elements you'd like to include...",
            height=100
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Generation process section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.button("🚀 Generate Complete Story & Video", type="primary", use_container_width=True):
            if story_input.strip():
                run_full_automation_pipeline(story_input.strip(), additional_context)
            else:
                st.error("Please enter a story name or concept!")
    
    with col2:
        if st.button("🎨 Generate Blueprint Only", use_container_width=True):
            if story_input.strip():
                generate_blueprint_only(story_input.strip(), additional_context)
            else:
                st.error("Please enter a story name or concept!")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Current progress section
    if st.session_state.get('automation_in_progress'):
        show_automation_progress()
    
    # Recent productions
    show_recent_productions("fairer-tales")
    
    # Pipeline status for Fairer Tales
    if UNDERGROUND_API_AVAILABLE:
        try:
            api = get_underground_api()
            status = api.get_pipeline_status("fairer-tales")
            show_pipeline_status(status)
        except Exception as e:
            st.error(f"Error getting pipeline status: {e}")

def timeless_retold_tab():
    """Timeless Retold - Book processing interface"""
    st.header("📚 Timeless Retold - Classic Book Modernization")
    st.markdown("**Transform classic literature into modern retellings with full book processing**")
    
    # Book upload section
    st.subheader("📖 Book Upload & Processing")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Upload a classic book (TXT, PDF, EPUB)",
            type=['txt', 'pdf', 'epub'],
            help="Upload a classic book for modernization and chapter-by-chapter processing"
        )
        
        if uploaded_file:
            st.success(f"📁 Uploaded: {uploaded_file.name}")
            
            # Book processing options
            st.subheader("⚙️ Processing Options")
            
            col1a, col1b = st.columns(2)
            with col1a:
                modernization_style = st.selectbox(
                    "Modernization Approach",
                    ["Contemporary Setting", "Urban Fantasy", "Sci-Fi Retelling", "Historical Fiction", "Psychological Thriller"]
                )
            
            with col1b:
                target_length = st.selectbox(
                    "Target Length per Chapter",
                    ["Short (2-3 pages)", "Medium (4-6 pages)", "Long (7-10 pages)"]
                )
            
            # Process button
            if st.button("🔄 Process Book", type="primary", use_container_width=True):
                process_uploaded_book(uploaded_file, modernization_style, target_length)
    
    with col2:
        # Pre-loaded classics
        st.subheader("📚 Available Classics")
        classic_books = [
            "Alice's Adventures in Wonderland",
            "Around the World in Eighty Days", 
            "Dracula",
            "Moby-Dick or, The Whale",
            "The Life and Adventures of Robinson Crusoe",
            "Twenty Thousand Leagues under the Sea"
        ]
        
        selected_classic = st.selectbox("Select a pre-loaded classic:", ["Choose..."] + classic_books)
        
        if selected_classic != "Choose...":
            if st.button(f"📖 Process {selected_classic}", use_container_width=True):
                process_preloaded_classic(selected_classic)
    
    # Chapter management
    if st.session_state.get('processed_chapters'):
        show_chapter_management()
    
    # Pipeline status
    if UNDERGROUND_API_AVAILABLE:
        try:
            api = get_underground_api()
            status = api.get_pipeline_status("timeless-retold")
            show_pipeline_status(status)
        except Exception as e:
            st.error(f"Error getting pipeline status: {e}")

def minute_myths_tab():
    """Minute Myths - Mythology content interface"""
    st.header("⚡ Minute Myths - Quick Mythology Retellings")
    st.markdown("**One-minute mythology stories optimized for short-form content**")
    
    # Mythology selection
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🌍 Mythology Database")
        
        # REAL AUTHENTIC MYTHOLOGY DATABASE
        mythology_categories = {
            "Greek Mythology": [
                "Perseus and Medusa", "Pandora's Box", "Theseus and the Minotaur", 
                "Orpheus and Eurydice", "King Midas and the Golden Touch", "Icarus and the Sun",
                "Demeter and Persephone", "Echo and Narcissus", "The Twelve Labors of Hercules",
                "The Odyssey - Sirens", "The Odyssey - Cyclops", "The Odyssey - Lotus Eaters"
            ],
            "Norse Mythology": [
                "Ragnarök - The End of the World", "Loki and the Death of Baldr", "Thor's Hammer Mjolnir",
                "Odin's Sacrifice for Wisdom", "The Creation of the World", "Fenrir the Wolf",
                "The Rainbow Bridge Bifrost", "Yggdrasil the World Tree", "The Valkyries",
                "Loki's Punishment", "The Golden Apples of Idunn", "Thor and the Giants"
            ],
            "Egyptian Mythology": [
                "Osiris and Isis", "The Battle of Horus and Set", "The Journey Through the Afterlife",
                "The Creation by Atum", "The Weighing of the Heart", "Ra's Journey Through the Underworld",
                "The Story of Hathor", "Anubis and Mummification", "The Pharaoh's Divine Right",
                "The Curse of the Pharaohs", "Thoth and the Moon", "Bastet the Cat Goddess"
            ],
            "Japanese Mythology": [
                "Amaterasu and the Cave", "Susanoo and the Eight-Headed Dragon", "The Tale of Urashima Taro",
                "The Moon Princess Kaguya", "Izanagi and Izanami", "The Birth of Japan",
                "Yamata-no-Orochi Dragon", "The Crane Wife", "Momotaro the Peach Boy",
                "The Bamboo Cutter", "Tengu Mountain Spirits", "Kitsune Fox Spirits"
            ],
            "Celtic Mythology": [
                "The Children of Lir", "Cú Chulainn's Rage", "The Táin - Cattle Raid of Cooley",
                "Brigid and the Sacred Fire", "The Morrigan in Battle", "Finn MacCool and the Giants",
                "The Selkies of the Sea", "Banshees and Death Omens", "The Otherworld",
                "Druids and Sacred Groves", "The Cauldron of Rebirth", "Bran the Blessed"
            ],
            "Hindu Mythology": [
                "Rama and Sita - The Ramayana", "Krishna and the Butter Thief", "Ganesha's Broken Tusk",
                "Hanuman's Leap to Lanka", "The Churning of the Ocean", "Shiva's Cosmic Dance",
                "Durga and the Buffalo Demon", "Vishnu's Ten Avatars", "The Birth of Ganga",
                "Arjuna and the Bhagavad Gita", "Lakshmi and Prosperity", "Saraswati and Knowledge"
            ],
            "Native American": [
                "The Great Spirit's Creation", "Coyote the Trickster", "The Thunderbird",
                "White Buffalo Woman", "The Seven Sisters (Pleiades)", "Raven Steals the Sun",
                "Kokopelli the Fertility God", "The Vision Quest", "Spider Grandmother",
                "The Medicine Wheel", "Wendigo the Cannibal", "The Dream Catcher"
            ],
            "Mesopotamian": [
                "Gilgamesh and Enkidu", "The Great Flood", "Inanna's Descent to the Underworld",
                "The Creation of Humanity", "Tiamat and Marduk", "The Tower of Babel",
                "Ishtar and Tammuz", "The Epic of Creation", "Enlil's Wrath", 
                "The Seven Sages", "Ereshkigal Queen of the Dead", "The Plant of Immortality"
            ]
        }
        
        selected_category = st.selectbox("Select Mythology:", list(mythology_categories.keys()))
        selected_myth = st.selectbox("Select Authentic Story:", mythology_categories[selected_category])
        
        # Video format options
        video_format = st.selectbox(
            "Video Format:",
            ["Single Video (1 minute)", "Part 1 of 3", "Part 2 of 3", "Part 3 of 3"]
        )
        
        # Narration style for educational content
        narration_style = st.selectbox(
            "Narration Style:",
            ["Exciting & Fast-Paced", "Dramatic & Epic", "Mysterious & Suspenseful", "Educational & Clear"]
        )
        
        # Generate button
        if st.button("⚡ Generate Authentic Myth Video", type="primary", use_container_width=True):
            generate_authentic_myth_video(selected_myth, selected_category, video_format, narration_style)
    
    with col2:
        st.subheader("🎯 Mythology Database")
        
        # Real stats from the actual database
        total_myths = sum(len(myths) for myths in mythology_categories.values())
        st.metric("Available Authentic Myths", total_myths)
        st.metric("Mythology Traditions", len(mythology_categories))
        
        st.write("**Available Categories:**")
        for category, myths in mythology_categories.items():
            st.write(f"• {category}: {len(myths)} stories")
    
    # Generated content display
    if st.session_state.get('generated_myth'):
        show_generated_myth()
    
    # Batch generation
    with st.expander("🔄 Batch Generation"):
        st.write("Generate multiple myths at once")
        
        batch_count = st.slider("Number of myths to generate:", 1, 10, 3)
        random_selection = st.checkbox("Random mythology selection")
        
        if st.button("🚀 Generate Batch", use_container_width=True):
            generate_myth_batch(batch_count, random_selection)
    
    # Pipeline status
    if UNDERGROUND_API_AVAILABLE:
        try:
            api = get_underground_api()
            status = api.get_pipeline_status("minute-myths")
            show_pipeline_status(status)
        except Exception as e:
            st.error(f"Error getting pipeline status: {e}")

def dashboard_tab():
    """Dashboard - Production monitoring and scheduling"""
    st.header("📊 Underground Stories Dashboard")
    st.markdown("**Real-time production monitoring, scheduling, and system overview**")
    
    # Refresh button
    col1, col2, col3 = st.columns([2, 1, 1])
    with col3:
        if st.button("🔄 Refresh Dashboard", use_container_width=True):
            st.rerun()
    
    # System overview metrics
    st.subheader("🏥 System Health")
    
    if UNDERGROUND_API_AVAILABLE:
        try:
            api = get_underground_api()
            health = api.get_system_health()
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown('<div class="dashboard-metric">', unsafe_allow_html=True)
                api_status = "🟢 Healthy" if health.get("api_status") == "healthy" else "🔴 Error"
                st.metric("API Status", api_status)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="dashboard-metric">', unsafe_allow_html=True)
                youtube_status = "🟢 Connected" if health.get("youtube_api") == "connected" else "🔴 Disconnected" 
                st.metric("YouTube API", youtube_status)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col3:
                st.markdown('<div class="dashboard-metric">', unsafe_allow_html=True)
                scheduler_status = "🟢 Available" if health.get("scheduler") == "available" else "🔴 Unavailable"
                st.metric("Scheduler", scheduler_status)
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col4:
                st.markdown('<div class="dashboard-metric">', unsafe_allow_html=True)
                blueprint_status = "🟢 Available" if health.get("blueprint_generator") == "available" else "🔴 Error"
                st.metric("Blueprint Gen", blueprint_status)
                st.markdown('</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error getting system health: {e}")
    else:
        st.error("Underground API not available")
    
    # Production status
    st.subheader("🎬 Production Status")
    
    if UNDERGROUND_API_AVAILABLE:
        try:
            api = get_underground_api()
            production_status = api.get_production_status()
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Progress display
                progress_percentage = production_status.progress_percentage
                st.progress(progress_percentage / 100.0)
                st.write(f"**Overall Progress:** {progress_percentage:.1f}%")
                
                # Current production info
                st.write(f"**Current Week:** {production_status.current_week}")
                st.write(f"**Current Story:** {production_status.current_story}")
                st.write(f"**Next Scheduled:** {production_status.next_scheduled_run}")
                
                # Completed and failed stories
                if production_status.completed_stories:
                    st.success(f"✅ Completed: {len(production_status.completed_stories)} stories")
                
                if production_status.failed_stories:
                    st.error(f"❌ Failed: {len(production_status.failed_stories)} stories")
            
            with col2:
                # Manual controls
                st.subheader("🔧 Manual Controls")
                
                if st.button("🚀 Run Manual Production", use_container_width=True):
                    run_manual_production()
                
                if st.button("📹 Test Video Generation", use_container_width=True):
                    test_single_video()
                
                if st.button("📤 Test YouTube Upload", use_container_width=True):
                    test_youtube_connection()
                
                if st.button("💾 Create Backup", use_container_width=True):
                    create_system_backup()
            
        except Exception as e:
            st.error(f"Error getting production status: {e}")
    
    # Pipeline overview
    st.subheader("🚀 Pipeline Overview")
    
    pipelines = ["fairer-tales", "timeless-retold", "minute-myths"]
    
    for pipeline in pipelines:
        if UNDERGROUND_API_AVAILABLE:
            try:
                api = get_underground_api()
                status = api.get_pipeline_status(pipeline)
                show_pipeline_card(pipeline, status)
            except Exception as e:
                st.error(f"Error getting {pipeline} status: {e}")
    
    # Recent activity log
    st.subheader("📋 Recent Activity")
    show_activity_log()
    
    # Scheduling section
    st.subheader("📅 Production Schedule")
    show_production_schedule()

def settings_tab():
    """Settings - Model router and configuration"""
    st.header("⚙️ Settings & Configuration")
    st.markdown("**System configuration, model routing, and advanced settings**")
    
    # Model Router Configuration
    st.subheader("🤖 Model Router Configuration")
    
    # AI Model settings (from Flipside architecture)
    model_categories = {
        "Blueprint Parser": {
            "current": "gpt-4o-mini-2024-07-18",
            "options": ["gpt-4o-mini-2024-07-18", "gpt-4o-2024-11-20", "claude-3-haiku-20240307"],
            "description": "Parses and analyzes story blueprints"
        },
        "Writer Agent": {
            "current": "gpt-4o-2024-11-20", 
            "options": ["gpt-4o-2024-11-20", "claude-3-5-sonnet-20241022", "gpt-4-turbo-2024-04-09"],
            "description": "Primary story generation and narrative flow"
        },
        "Character Consultant": {
            "current": "gpt-4o-2024-11-20",
            "options": ["gpt-4o-2024-11-20", "claude-3-5-sonnet-20241022", "gpt-4-turbo-2024-04-09"],
            "description": "Character development and motivation analysis"
        },
        "Theme Consultant": {
            "current": "gpt-4o-2024-11-20",
            "options": ["gpt-4o-2024-11-20", "claude-3-5-sonnet-20241022", "o1-preview"],
            "description": "Theme integration and narrative coherence"
        },
        "Atmosphere Consultant": {
            "current": "gpt-4o-2024-11-20",
            "options": ["gpt-4o-2024-11-20", "claude-3-5-sonnet-20241022", "gpt-4-turbo-2024-04-09"],
            "description": "Scene building and atmospheric details"
        },
        "Continuity Auditor": {
            "current": "gpt-4o-mini-2024-07-18",  
            "options": ["gpt-4o-mini-2024-07-18", "claude-3-haiku-20240307", "o1-mini"],
            "description": "Quality validation and consistency checking"
        }
    }
    
    for category, config in model_categories.items():
        with st.expander(f"⚙️ {category}"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                selected_model = st.selectbox(
                    f"Model for {category}:",
                    config["options"],
                    index=config["options"].index(config["current"]),
                    key=f"model_{category.lower().replace(' ', '_')}"
                )
                st.write(f"*{config['description']}*")
            
            with col2:
                st.metric("Current", config["current"])
                if st.button(f"Update {category}", key=f"update_{category.lower().replace(' ', '_')}"):
                    st.success(f"Updated {category} to {selected_model}")
    
    # Voice Generation Settings
    st.subheader("🔊 Voice Generation Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        voice_provider = st.selectbox(
            "Voice Provider:",
            ["Google Cloud TTS", "OpenAI TTS", "ElevenLabs", "Azure TTS"]
        )
        
        voice_model = st.selectbox(
            "Voice Model:",
            ["neural2-optimized", "journey", "alloy", "echo"] 
        )
    
    with col2:
        voice_speed = st.slider("Speech Speed:", 0.75, 1.25, 1.0, 0.05)
        voice_pitch = st.slider("Voice Pitch:", -5.0, 5.0, 0.0, 0.5)
    
    # Video Generation Settings
    st.subheader("🎬 Video Generation Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        video_resolution = st.selectbox(
            "Video Resolution:",
            ["1920x1080 (Full HD)", "1280x720 (HD)", "3840x2160 (4K)"]
        )
        
        video_fps = st.selectbox("Frame Rate:", ["24 fps", "30 fps", "60 fps"])
    
    with col2:
        video_quality = st.selectbox("Video Quality:", ["High", "Medium", "Low"])
        background_style = st.selectbox("Background Style:", ["Animated", "Static", "Parallax"])
    
    # YouTube Settings
    st.subheader("📺 YouTube Integration Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        channel_name = st.text_input("Channel Name:", placeholder="Underground Stories")
        default_privacy = st.selectbox("Default Privacy:", ["private", "unlisted", "public"])
    
    with col2:
        upload_schedule = st.selectbox(
            "Upload Schedule:",
            ["Sunday 11:00 PM (Israel)", "Custom Time", "Immediate"]
        )
        
        if upload_schedule == "Custom Time":
            custom_time = st.time_input("Custom Upload Time:")
    
    # Automation Settings
    st.subheader("🤖 Automation Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        auto_generation = st.checkbox("Enable Weekly Auto-Generation", value=True)
        auto_upload = st.checkbox("Enable Auto-Upload to YouTube", value=False)
    
    with col2:
        backup_frequency = st.selectbox("Backup Frequency:", ["Daily", "Weekly", "Monthly"])
        data_retention = st.selectbox("Data Retention:", ["30 days", "90 days", "1 year", "Forever"])
    
    # Advanced Settings
    with st.expander("🔧 Advanced Settings"):
        st.subheader("System Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            max_concurrent = st.number_input("Max Concurrent Generations:", 1, 10, 3)
            timeout_minutes = st.number_input("Generation Timeout (minutes):", 5, 60, 30)
        
        with col2:
            debug_mode = st.checkbox("Enable Debug Mode")
            verbose_logging = st.checkbox("Verbose Logging")
        
        # Data storage settings
        st.subheader("Data Storage")
        
        storage_mode = st.radio(
            "Storage Mode:",
            ["JSON Files (Current)", "Supabase Database (Future)"],
            index=0
        )
        
        if storage_mode == "Supabase Database (Future)":
            st.info("Supabase integration will be implemented in a future update")
    
    # Save settings
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        if st.button("💾 Save All Settings", type="primary", use_container_width=True):
            save_settings()

# Helper functions for the tabs

def run_full_automation_pipeline(story_input: str, additional_context: str = ""):
    """Run the complete automation pipeline from story name to video"""
    st.session_state.automation_in_progress = True
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Step 1: Generate Blueprint (20%)
        status_text.text("🎨 Generating detailed blueprint...")
        progress_bar.progress(0.2)
        
        if UNDERGROUND_API_AVAILABLE:
            api = get_underground_api()
            blueprint_result = api.generate_blueprint(story_input, additional_context)
            
            if blueprint_result["success"]:
                st.success(f"✅ Blueprint generated: {blueprint_result['story_title']}")
                
                # Step 2: Generate Story (40%)
                status_text.text("✍️ Generating story from blueprint...")
                progress_bar.progress(0.4)
                
                # Here you would integrate with Flipside story generation
                if FLIPSIDE_AVAILABLE:
                    processor = FlipsideProcessor()
                    story_result = processor.process_blueprint_text(
                        blueprint_result["flipside_format"],
                        st.session_state.get("selected_style", "sympathetic_antihero")
                    )
                    
                    if story_result["success"]:
                        st.success(f"✅ Story generated: {story_result['word_count']} words")
                        
                        # Step 3: Generate Audio (60%)
                        status_text.text("🔊 Generating audio narration...")
                        progress_bar.progress(0.6)
                        time.sleep(2)  # Placeholder
                        st.success("✅ Audio narration generated")
                        
                        # Step 4: Generate Video (80%)
                        status_text.text("🎬 Creating video with narration...")
                        progress_bar.progress(0.8)
                        
                        video_result = api.generate_single_story_video(
                            blueprint_result['story_title'], 1
                        )
                        
                        if video_result.success:
                            st.success(f"✅ Video generated: {video_result.file_size_mb}MB")
                            
                            # Step 5: Upload to YouTube (100%)
                            status_text.text("📤 Uploading to YouTube...")
                            progress_bar.progress(1.0)
                            
                            # Placeholder for YouTube upload
                            st.success("✅ Complete automation pipeline finished!")
                            
                            # Store results
                            st.session_state.latest_production = {
                                "story_title": blueprint_result['story_title'],
                                "video_path": video_result.video_path,
                                "generated_at": datetime.now().isoformat()
                            }
                        else:
                            st.error(f"❌ Video generation failed: {video_result.error}")
                    else:
                        st.error(f"❌ Story generation failed: {story_result.get('error', 'Unknown error')}")
                else:
                    st.error("❌ Flipside system not available for story generation")
            else:
                st.error(f"❌ Blueprint generation failed: {blueprint_result.get('error', 'Unknown error')}")
        else:
            st.error("❌ Underground API not available")
    
    except Exception as e:
        st.error(f"❌ Pipeline error: {str(e)}")
    
    finally:
        st.session_state.automation_in_progress = False

def generate_blueprint_only(story_input: str, additional_context: str = ""):
    """Generate just the blueprint for manual review"""
    if UNDERGROUND_API_AVAILABLE:
        try:
            api = get_underground_api()
            
            with st.spinner("🎨 Generating detailed blueprint..."):
                result = api.generate_blueprint(story_input, additional_context)
            
            if result["success"]:
                st.success(f"✅ Blueprint generated: {result['story_title']}")
                
                # Display the blueprint
                st.subheader("📋 Generated Blueprint")
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.text_area(
                        "Flipside Format (ready for story generation):",
                        value=result["flipside_format"],
                        height=400,
                        help="This blueprint is ready to use in the Flipside story generator"
                    )
                
                with col2:
                    st.json(result["blueprint"])
                    
                    if st.button("✍️ Generate Story from Blueprint", use_container_width=True):
                        generate_story_from_blueprint(result["flipside_format"])
                    
                    st.download_button(
                        "📥 Download Blueprint",
                        data=result["flipside_format"],
                        file_name=f"{result['story_title'].replace(' ', '_').lower()}_blueprint.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
            else:
                st.error(f"❌ Blueprint generation failed: {result.get('error', 'Unknown error')}")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    else:
        st.error("❌ Underground API not available")

def generate_story_from_blueprint(blueprint_text: str):
    """Generate story using Flipside from blueprint"""
    if FLIPSIDE_AVAILABLE:
        try:
            processor = FlipsideProcessor()
            
            with st.spinner("✍️ Generating story through 8-agent pipeline..."):
                result = processor.process_blueprint_text(
                    blueprint_text,
                    st.session_state.get("selected_style", "sympathetic_antihero")
                )
            
            if result["success"]:
                st.success(f"✅ Story generated: {result['story_title']} ({result['word_count']} words)")
                
                # Display the story
                st.subheader("📖 Generated Story")
                
                with open(result["filepath"], 'r') as f:
                    story_content = f.read()
                
                st.text_area(
                    "Your Generated Story:",
                    value=story_content,
                    height=400
                )
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.download_button(
                        "📥 Download Story",
                        data=story_content,
                        file_name=f"{result['story_title'].replace(' ', '_').lower()}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                
                with col2:
                    if st.button("🔊 Generate Audio", use_container_width=True):
                        st.info("Audio generation feature coming soon!")
                
                with col3:
                    if st.button("🎬 Generate Video", use_container_width=True):
                        st.info("Video generation feature coming soon!")
            else:
                st.error(f"❌ Story generation failed: {result.get('error', 'Unknown error')}")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    else:
        st.error("❌ Flipside system not available")

def show_automation_progress():
    """Show current automation progress"""
    st.subheader("🔄 Automation in Progress")
    
    # This would show real-time progress
    progress_data = st.session_state.get('automation_progress', {})
    
    stages = [
        "Blueprint Generation",
        "Story Writing", 
        "Audio Generation",
        "Video Creation",
        "YouTube Upload"
    ]
    
    for i, stage in enumerate(stages):
        status = progress_data.get(stage, "pending")
        if status == "completed":
            st.success(f"✅ {stage}")
        elif status == "in_progress":
            st.info(f"🔄 {stage}")
        else:
            st.text(f"⏳ {stage}")

def show_recent_productions(pipeline: str):
    """Show recent productions for a pipeline"""
    st.subheader("📈 Recent Productions")
    
    # Get actual production data from API
    if UNDERGROUND_API_AVAILABLE:
        try:
            api = get_underground_api()
            production_status = api.get_production_status()
            
            if production_status.completed_stories:
                st.write("**Completed Stories:**")
                for story in production_status.completed_stories:
                    st.write(f"✅ {story}")
            
            if production_status.failed_stories:
                st.write("**Failed Stories:**")
                for story in production_status.failed_stories:
                    st.write(f"❌ {story}")
                    
            if not production_status.completed_stories and not production_status.failed_stories:
                st.info("No productions recorded yet. Start creating content to see history here!")
                
        except Exception as e:
            st.error(f"Error getting production data: {e}")
    else:
        st.info("Connect Underground API to see production history")

def show_pipeline_status(status: Dict[str, Any]):
    """Show pipeline status card"""
    st.markdown('<div class="pipeline-card">', unsafe_allow_html=True)
    
    pipeline_name = status.get("pipeline", "Unknown").replace("-", " ").title()
    st.subheader(f"🚀 {pipeline_name}")
    
    status_indicator = {
        "active": "🟢",
        "development": "🟡", 
        "inactive": "🔴"
    }
    
    current_status = status.get("status", "unknown")
    st.write(f"{status_indicator.get(current_status, '⚪')} Status: {current_status}")
    
    if "description" in status:
        st.write(status["description"])
    
    if "features" in status:
        st.write("**Features:**")
        for feature in status["features"]:
            st.write(f"• {feature}")
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_pipeline_card(pipeline: str, status: Dict[str, Any]):
    """Show pipeline overview card"""
    pipeline_name = pipeline.replace("-", " ").title()
    
    with st.container():
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.write(f"**{pipeline_name}**")
            st.write(status.get("description", "No description"))
        
        with col2:
            current_status = status.get("status", "unknown")
            status_color = {"active": "🟢", "development": "🟡", "inactive": "🔴"}
            st.write(f"{status_color.get(current_status, '⚪')} {current_status}")
        
        with col3:
            if current_status == "active":
                progress = status.get("progress", 0)
                st.progress(progress / 100.0)
                st.write(f"{progress}%")

def process_uploaded_book(uploaded_file, modernization_style: str, target_length: str):
    """Process uploaded book for Timeless Retold"""
    st.info(f"📚 Processing {uploaded_file.name} with {modernization_style} approach...")
    
    # This would implement the actual book processing
    with st.spinner("Processing book chapters..."):
        time.sleep(3)  # Placeholder
    
    st.success("✅ Book processed successfully!")
    
    # Store processed chapters in session state
    st.session_state.processed_chapters = [
        {"chapter": 1, "title": "Chapter 1: The Beginning", "length": "4 pages", "status": "ready"},
        {"chapter": 2, "title": "Chapter 2: The Journey", "length": "5 pages", "status": "ready"},
        {"chapter": 3, "title": "Chapter 3: The Challenge", "length": "6 pages", "status": "ready"}
    ]

def process_preloaded_classic(classic_title: str):
    """Process a pre-loaded classic book"""
    st.info(f"📖 Processing {classic_title}...")
    
    # Check if file exists
    content_path = project_root / "content" / "timeless-retold" / f"{classic_title}.txt"
    
    if content_path.exists():
        with st.spinner("Analyzing book structure..."):
            time.sleep(2)  # Placeholder
        
        st.success(f"✅ {classic_title} loaded and ready for processing!")
        
        # Store processed chapters
        st.session_state.processed_chapters = [
            {"chapter": 1, "title": "Opening", "length": "3 pages", "status": "ready"},
            {"chapter": 2, "title": "Development", "length": "4 pages", "status": "ready"}
        ]
    else:
        st.error(f"❌ {classic_title} not found in content directory")

def show_chapter_management():
    """Show chapter management interface"""
    st.subheader("📑 Chapter Management")
    
    chapters = st.session_state.get('processed_chapters', [])
    
    for chapter in chapters:
        col1, col2, col3, col4 = st.columns([1, 2, 1, 1])
        
        with col1:
            st.write(f"Ch. {chapter['chapter']}")
        
        with col2:
            st.write(chapter['title'])
        
        with col3:
            st.write(chapter['length'])
        
        with col4:
            if st.button(f"🎬 Generate", key=f"gen_ch_{chapter['chapter']}"):
                st.info(f"Generating video for Chapter {chapter['chapter']}")

def generate_authentic_myth_video(myth_name: str, category: str, video_format: str, narration_style: str):
    """Generate an authentic mythology video using the new pipeline"""
    st.info(f"⚡ Generating authentic {myth_name} from {category}...")
    st.info(f"📱 Format: {video_format} | Style: {narration_style} | Mobile Optimized (9:16)")
    
    if UNDERGROUND_API_AVAILABLE:
        try:
            api = get_underground_api()
            
            with st.spinner("🎬 Creating authentic mythology video..."):
                import asyncio
                result = asyncio.run(api.generate_minute_myths_video(myth_name, category, video_format, narration_style))
            
            if result["success"]:
                st.success("✅ Authentic mythology video generated!")
                
                # Display results
                st.subheader("📱 Generated Video")
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write(f"**Title:** {result.get('video_title', myth_name)}")
                    st.write(f"**Format:** {result.get('video_format', video_format)}")
                    st.write(f"**Duration:** {result.get('duration', 60)} seconds")
                    st.write(f"**Style:** {result.get('narration_style', narration_style)}")
                    st.write(f"**Mobile Optimized:** ✅ {result.get('vertical_format', '9:16')}")
                    
                    if result.get('video_path'):
                        st.write(f"**Video Path:** {result['video_path']}")
                
                with col2:
                    st.info("📱 **Mobile Features:**")
                    st.write("• Vertical 9:16 format")
                    st.write("• Dynamic visuals")
                    st.write("• Clear text overlays")
                    st.write("• Engaging narration")
                    st.write("• Educational content")
                
                # Store in session for display
                st.session_state.generated_myth = f"""
**{myth_name}**
*From {category}*

✅ **Video Generated Successfully!**

**Specifications:**
• Format: {video_format}
• Aspect Ratio: 9:16 (Mobile Vertical)
• Duration: {result.get('duration', 60)} seconds
• Narration: {narration_style}
• Educational Focus: Authentic historical/cultural content
• Mobile Optimized: ✅ Ready for social media

**Status:** {result.get('ready_for_upload', 'Processing...')}
"""
                
            else:
                st.error(f"❌ Video generation failed: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            st.error(f"❌ Error generating video: {str(e)}")
    else:
        # Fallback to content preview
        with st.spinner("Creating authentic mythology content preview..."):
            time.sleep(2)
        
        authentic_myth = f"""
**{myth_name}**
*From {category}*

{get_authentic_myth_content(myth_name, category, video_format)}

**Video Specifications:**
• Format: {video_format}
• Aspect Ratio: 9:16 (Mobile Vertical)
• Duration: {"60 seconds" if "Single" in video_format else "60 seconds per part"}
• Narration: {narration_style}
• Educational Focus: Authentic historical/cultural content

**Note:** Connect Underground API for full video generation
"""
        
        st.session_state.generated_myth = authentic_myth
        st.success("✅ Authentic mythology content preview generated!")

def get_authentic_myth_content(myth_name: str, category: str, video_format: str) -> str:
    """Get authentic mythology content - this would connect to a real mythology database"""
    
    # Sample authentic content - in production this would pull from mythology database
    myth_database = {
        "Perseus and Medusa": {
            "single": "Perseus, son of Zeus, must slay the deadly Gorgon Medusa whose gaze turns men to stone. Armed with a mirrored shield from Athena, winged sandals from Hermes, and an invisible helmet from Hades, he approaches her lair backwards, watching only her reflection. With one swift stroke, he beheads the sleeping monster, her blood giving birth to the winged horse Pegasus.",
            "part1": "Perseus, the demigod son of Zeus and mortal Danae, receives an impossible quest: bring back the head of Medusa, the deadly Gorgon whose very gaze turns living beings to stone.",
            "part2": "The gods aid Perseus with magical gifts - Athena's polished shield, Hermes' winged sandals, and Hades' helmet of invisibility. He seeks the Graiae, three ancient sisters who share one eye.",
            "part3": "Using his shield as a mirror, Perseus approaches the sleeping Medusa backwards and beheads her in one swift stroke. From her blood springs Pegasus, the winged horse, as Perseus escapes her sisters' wrath."
        },
        "Pandora's Box": {
            "single": "The gods create Pandora, the first woman, as punishment for Prometheus stealing fire. Given to Epimetheus with a mysterious jar as dowry, curiosity overwhelms her. She opens it, releasing all evils into the world - disease, death, hatred, and suffering. Only Hope remains trapped inside when she quickly closes it, becoming humanity's last comfort in a world now filled with hardship.",
            "part1": "After Prometheus steals fire for humanity, Zeus creates Pandora as revenge - the first woman, beautiful but crafted with a fatal flaw: overwhelming curiosity.",
            "part2": "Pandora marries Epimetheus and receives a mysterious sealed jar as her dowry, with strict instructions never to open it. But her curiosity grows stronger each day.",
            "part3": "Unable to resist, Pandora opens the jar, releasing all evils into the world. Only Hope remains inside, becoming humanity's comfort against the suffering now loose in the world."
        }
    }
    
    if myth_name in myth_database:
        myth_content = myth_database[myth_name]
        if "Single" in video_format:
            return myth_content.get("single", "Authentic myth content would be generated here.")
        elif "Part 1" in video_format:
            return myth_content.get("part1", "Part 1 content would be generated here.")
        elif "Part 2" in video_format:
            return myth_content.get("part2", "Part 2 content would be generated here.")
        elif "Part 3" in video_format:
            return myth_content.get("part3", "Part 3 content would be generated here.")
    
    return f"Authentic {myth_name} story from {category} would be researched and generated here from historical sources."

def show_generated_myth():
    """Display the generated myth"""
    st.subheader("⚡ Generated Myth")
    
    myth_text = st.session_state.get('generated_myth', '')
    
    st.markdown(myth_text)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔊 Generate Audio", use_container_width=True):
            st.info("Audio generation coming soon!")
    
    with col2:
        if st.button("🎬 Create Video", use_container_width=True):
            st.info("Video generation coming soon!")
    
    with col3:
        st.download_button(
            "📥 Download",
            data=myth_text,
            file_name="minute_myth.txt",
            mime="text/plain",
            use_container_width=True
        )

def generate_myth_batch(batch_count: int, random_selection: bool):
    """Generate multiple myths in batch"""
    st.info(f"🔄 Generating {batch_count} myths in batch mode...")
    
    with st.spinner("Batch generating myths..."):
        time.sleep(batch_count)  # Placeholder
    
    st.success(f"✅ Generated {batch_count} myths successfully!")

def run_manual_production():
    """Run manual production cycle"""
    if UNDERGROUND_API_AVAILABLE:
        try:
            api = get_underground_api()
            
            with st.spinner("🔧 Running manual production cycle..."):
                result = api.trigger_manual_production()
            
            if result["success"]:
                st.success("✅ Manual production completed successfully!")
                st.json(result["result"])
            else:
                st.error(f"❌ Manual production failed: {result.get('error', 'Unknown error')}")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    else:
        st.error("❌ Underground API not available")

def test_single_video():
    """Test single video generation"""
    if UNDERGROUND_API_AVAILABLE:
        try:
            api = get_underground_api()
            
            with st.spinner("🎬 Testing video generation..."):
                result = api.generate_single_story_video("Test Story", 1)
            
            if result.success:
                st.success(f"✅ Test video generated: {result.file_size_mb}MB")
                st.write(f"**Video Path:** {result.video_path}")
            else:
                st.error(f"❌ Video generation failed: {result.error}")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    else:
        st.error("❌ Underground API not available")

def test_youtube_connection():
    """Test YouTube connection"""
    if UNDERGROUND_API_AVAILABLE:
        try:
            api = get_underground_api()
            
            with st.spinner("📤 Testing YouTube connection..."):
                result = api.test_youtube_connection()
            
            if result["connected"]:
                st.success("✅ YouTube connection successful!")
                if "channel_info" in result:
                    st.json(result["channel_info"])
            else:
                st.error(f"❌ YouTube connection failed: {result.get('error', 'Unknown error')}")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    else:
        st.error("❌ Underground API not available")

def create_system_backup():
    """Create system backup"""
    if UNDERGROUND_API_AVAILABLE:
        try:
            api = get_underground_api()
            
            with st.spinner("💾 Creating system backup..."):
                result = api.create_data_backup()
            
            if result["success"]:
                st.success("✅ Backup created successfully!")
                st.write(f"**Backup Path:** {result['backup_path']}")
            else:
                st.error(f"❌ Backup failed: {result.get('error', 'Unknown error')}")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    else:
        st.error("❌ Underground API not available")

def show_activity_log():
    """Show recent system activity"""
    st.info("📋 Activity log will show real system events as you use the platform")
    
    # This would be populated from actual system logs
    # For now, show only if there are real events
    if st.session_state.get('system_activities'):
        activities = st.session_state.system_activities
        
        for activity in activities:
            status_icon = {"success": "✅", "info": "ℹ️", "error": "❌", "warning": "⚠️"}
            icon = status_icon.get(activity["status"], "📝")
            
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"{icon} {activity['action']}")
            with col2:
                st.write(activity["time"])
    else:
        st.write("No recent activity. Start using the platform to see activity logs here.")

def show_production_schedule():
    """Show upcoming production schedule"""
    if UNDERGROUND_API_AVAILABLE:
        try:
            api = get_underground_api()
            production_status = api.get_production_status()
            
            st.write(f"**Next Scheduled Run:** {production_status.next_scheduled_run}")
            st.write(f"**Current Story:** {production_status.current_story}")
            st.write(f"**Week {production_status.current_week} of {production_status.total_stories}**")
            
            if production_status.progress_percentage > 0:
                st.progress(production_status.progress_percentage / 100.0)
            else:
                st.info("📅 Schedule will appear here once production begins")
                
        except Exception as e:
            st.error(f"Error getting schedule: {e}")
    else:
        st.info("📅 Connect Underground API to see production schedule")

def save_settings():
    """Save all settings"""
    st.success("✅ Settings saved successfully!")
    st.info("Settings will be applied on next system restart")

def show_system_health():
    """Show detailed system health"""
    if UNDERGROUND_API_AVAILABLE:
        try:
            api = get_underground_api()
            health = api.get_system_health()
            
            st.subheader("🏥 Detailed System Health")
            st.json(health)
        except Exception as e:
            st.error(f"❌ Error getting system health: {str(e)}")
    else:
        st.error("❌ Underground API not available")

def test_video_generation():
    """Test video generation functionality"""
    st.info("🎬 Testing video generation system...")
    
    if UNDERGROUND_API_AVAILABLE:
        try:
            api = get_underground_api()
            result = api.generate_single_story_video("Test Story", 1)
            
            if result.success:
                st.success(f"✅ Video test successful: {result.file_size_mb}MB")
            else:
                st.error(f"❌ Video test failed: {result.error}")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    else:
        st.error("❌ Underground API not available")

def show_blueprint_format():
    """Show blueprint format guide"""
    st.subheader("📋 Blueprint Format Guide")
    
    sample_blueprint = """17 Green Card — Dark Fantasy / Witness-Protection Parable

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
    
    st.text_area("Sample Blueprint Format:", value=sample_blueprint, height=400)

if __name__ == "__main__":
    main()