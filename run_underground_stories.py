#!/usr/bin/env python3
"""
Underground Stories - App Launcher
=================================

Quick launcher for the comprehensive Underground Stories platform.
Integrates Flipside architecture with video production capabilities.
"""

import subprocess
import sys
from pathlib import Path

def main():
    """Launch the Underground Stories comprehensive platform"""
    app_path = Path(__file__).parent / "web_app" / "underground_stories_app.py"
    
    print("🎬 Starting Underground Stories Platform...")
    print("=" * 60)
    print("📺 Comprehensive Video Production Platform")
    print("🧚 Fairer Tales - Full automation from story to video")
    print("📚 Timeless Retold - Classic book modernization")
    print("⚡ Minute Myths - Quick mythology retellings")
    print("📊 Dashboard - Production monitoring & scheduling")
    print("⚙️ Settings - Model routing & configuration")
    print("=" * 60)
    print(f"📱 App will open in your browser at: http://localhost:8502")
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 60)
    
    # Launch Streamlit on a different port to avoid conflicts
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", 
        str(app_path),
        "--server.port=8502",
        "--server.address=localhost",
        "--browser.gatherUsageStats=false"
    ])

if __name__ == "__main__":
    main()