#!/usr/bin/env python3
"""
Underground Stories Data Manager
===============================

Hybrid JSON/Supabase data management system.
Currently uses JSON with future Supabase migration capability.
"""

import json
import os
from typing import Dict, List, Optional, Any, Union
from pathlib import Path
from datetime import datetime
import asyncio
import logging

class DataManager:
    """
    Hybrid data manager supporting both JSON (current) and Supabase (future).
    Designed for easy migration when Supabase is reactivated.
    """
    
    def __init__(self, use_supabase: bool = False):
        self.use_supabase = use_supabase
        self.project_root = Path(__file__).parent.parent.parent.parent
        self.data_dir = self.project_root / "data"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        self.logger = logging.getLogger("DataManager")
        
        if use_supabase:
            self._init_supabase()
        else:
            self._init_json_storage()
    
    def _init_supabase(self):
        """Initialize Supabase connection (future implementation)"""
        # TODO: Implement when Supabase is reactivated
        self.logger.info("🔄 Supabase mode enabled (not yet implemented)")
        # from supabase import create_client, Client
        # self.supabase: Client = create_client(url, key)
        pass
    
    def _init_json_storage(self):
        """Initialize JSON file storage"""
        self.json_dir = self.data_dir / "json_storage"
        self.json_dir.mkdir(parents=True, exist_ok=True)
        self.logger.info(f"📁 JSON storage initialized: {self.json_dir}")
    
    # ========================================
    # Blueprint Management
    # ========================================
    
    def save_blueprint(self, blueprint_data: Dict[str, Any]) -> str:
        """Save blueprint data"""
        if self.use_supabase:
            return self._save_blueprint_supabase(blueprint_data)
        else:
            return self._save_blueprint_json(blueprint_data)
    
    def _save_blueprint_json(self, blueprint_data: Dict[str, Any]) -> str:
        """Save blueprint to JSON file"""
        story_id = blueprint_data.get("story_id", "unknown")
        title = blueprint_data.get("new", {}).get("title", "untitled")
        
        filename = f"blueprint_{story_id:02d}_{title.lower().replace(' ', '_').replace('&', 'and')}.json"
        filepath = self.project_root / "content" / "blueprints" / filename
        
        # Ensure directory exists
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(blueprint_data, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"💾 Blueprint saved: {filepath}")
        return str(filepath)
    
    def _save_blueprint_supabase(self, blueprint_data: Dict[str, Any]) -> str:
        """Save blueprint to Supabase (future implementation)"""
        # TODO: Implement Supabase storage
        self.logger.info("🔄 Saving blueprint to Supabase (not yet implemented)")
        return "supabase_id_placeholder"
    
    def load_blueprint(self, blueprint_id: Union[int, str]) -> Optional[Dict[str, Any]]:
        """Load blueprint data"""
        if self.use_supabase:
            return self._load_blueprint_supabase(blueprint_id)
        else:
            return self._load_blueprint_json(blueprint_id)
    
    def _load_blueprint_json(self, blueprint_id: Union[int, str]) -> Optional[Dict[str, Any]]:
        """Load blueprint from JSON file"""
        blueprints_dir = self.project_root / "content" / "blueprints"
        
        if isinstance(blueprint_id, int):
            # Search by story ID
            for blueprint_file in blueprints_dir.glob(f"blueprint_{blueprint_id:02d}_*.json"):
                try:
                    with open(blueprint_file, 'r', encoding='utf-8') as f:
                        return json.load(f)
                except Exception as e:
                    self.logger.error(f"Error loading blueprint {blueprint_file}: {e}")
                    continue
        else:
            # Search by exact filename
            blueprint_file = blueprints_dir / blueprint_id
            if blueprint_file.exists():
                try:
                    with open(blueprint_file, 'r', encoding='utf-8') as f:
                        return json.load(f)
                except Exception as e:
                    self.logger.error(f"Error loading blueprint {blueprint_file}: {e}")
        
        return None
    
    def _load_blueprint_supabase(self, blueprint_id: Union[int, str]) -> Optional[Dict[str, Any]]:
        """Load blueprint from Supabase (future implementation)"""
        # TODO: Implement Supabase loading
        self.logger.info(f"🔄 Loading blueprint {blueprint_id} from Supabase (not yet implemented)")
        return None
    
    def list_blueprints(self) -> List[Dict[str, Any]]:
        """List all available blueprints"""
        if self.use_supabase:
            return self._list_blueprints_supabase()
        else:
            return self._list_blueprints_json()
    
    def _list_blueprints_json(self) -> List[Dict[str, Any]]:
        """List blueprints from JSON files"""
        blueprints_dir = self.project_root / "content" / "blueprints"
        if not blueprints_dir.exists():
            return []
        
        blueprints = []
        for blueprint_file in blueprints_dir.glob("blueprint_*.json"):
            try:
                with open(blueprint_file, 'r', encoding='utf-8') as f:
                    blueprint_data = json.load(f)
                
                blueprints.append({
                    "story_id": blueprint_data.get("story_id"),
                    "title": blueprint_data.get("new", {}).get("title"),
                    "genre": blueprint_data.get("new", {}).get("genre"),
                    "filepath": str(blueprint_file),
                    "generated_at": blueprint_data.get("generated_at")
                })
            except Exception as e:
                self.logger.warning(f"⚠️ Error reading blueprint {blueprint_file}: {e}")
                continue
        
        return sorted(blueprints, key=lambda x: x.get("story_id", 0))
    
    def _list_blueprints_supabase(self) -> List[Dict[str, Any]]:
        """List blueprints from Supabase (future implementation)"""
        # TODO: Implement Supabase listing
        self.logger.info("🔄 Listing blueprints from Supabase (not yet implemented)")
        return []
    
    # ========================================
    # Session Management
    # ========================================
    
    def save_session(self, session_id: str, session_data: Dict[str, Any]) -> bool:
        """Save session data"""
        if self.use_supabase:
            return self._save_session_supabase(session_id, session_data)
        else:
            return self._save_session_json(session_id, session_data)
    
    def _save_session_json(self, session_id: str, session_data: Dict[str, Any]) -> bool:
        """Save session to JSON file"""
        try:
            session_file = self.data_dir / "underground_api" / f"session_{session_id}.json"
            session_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(session_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "session_id": session_id,
                    "data": session_data,
                    "saved_at": datetime.now().isoformat()
                }, f, indent=2)
            
            return True
        except Exception as e:
            self.logger.error(f"❌ Error saving session {session_id}: {e}")
            return False
    
    def _save_session_supabase(self, session_id: str, session_data: Dict[str, Any]) -> bool:
        """Save session to Supabase (future implementation)"""
        # TODO: Implement Supabase session storage
        self.logger.info(f"🔄 Saving session {session_id} to Supabase (not yet implemented)")
        return True
    
    def load_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Load session data"""
        if self.use_supabase:
            return self._load_session_supabase(session_id)
        else:
            return self._load_session_json(session_id)
    
    def _load_session_json(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Load session from JSON file"""
        try:
            session_file = self.data_dir / "underground_api" / f"session_{session_id}.json"
            
            if session_file.exists():
                with open(session_file, 'r', encoding='utf-8') as f:
                    session_data = json.load(f)
                return session_data.get("data")
            
            return None
        except Exception as e:
            self.logger.error(f"❌ Error loading session {session_id}: {e}")
            return None
    
    def _load_session_supabase(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Load session from Supabase (future implementation)"""
        # TODO: Implement Supabase session loading
        self.logger.info(f"🔄 Loading session {session_id} from Supabase (not yet implemented)")
        return None
    
    # ========================================
    # Production Data Management
    # ========================================
    
    def save_production_state(self, state_data: Dict[str, Any]) -> bool:
        """Save production state"""
        if self.use_supabase:
            return self._save_production_state_supabase(state_data)
        else:
            return self._save_production_state_json(state_data)
    
    def _save_production_state_json(self, state_data: Dict[str, Any]) -> bool:
        """Save production state to JSON file"""
        try:
            state_file = self.data_dir / "production_state.json"
            
            with open(state_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "state": state_data,
                    "updated_at": datetime.now().isoformat()
                }, f, indent=2)
            
            return True
        except Exception as e:
            self.logger.error(f"❌ Error saving production state: {e}")
            return False
    
    def _save_production_state_supabase(self, state_data: Dict[str, Any]) -> bool:
        """Save production state to Supabase (future implementation)"""
        # TODO: Implement Supabase production state storage
        self.logger.info("🔄 Saving production state to Supabase (not yet implemented)")
        return True
    
    def load_production_state(self) -> Optional[Dict[str, Any]]:
        """Load production state"""
        if self.use_supabase:
            return self._load_production_state_supabase()
        else:
            return self._load_production_state_json()
    
    def _load_production_state_json(self) -> Optional[Dict[str, Any]]:
        """Load production state from JSON file"""
        try:
            state_file = self.data_dir / "production_state.json"
            
            if state_file.exists():
                with open(state_file, 'r', encoding='utf-8') as f:
                    state_data = json.load(f)
                return state_data.get("state")
            
            return None
        except Exception as e:
            self.logger.error(f"❌ Error loading production state: {e}")
            return None
    
    def _load_production_state_supabase(self) -> Optional[Dict[str, Any]]:
        """Load production state from Supabase (future implementation)"""
        # TODO: Implement Supabase production state loading
        self.logger.info("🔄 Loading production state from Supabase (not yet implemented)")
        return None
    
    # ========================================
    # Migration Utilities (Future)
    # ========================================
    
    def migrate_to_supabase(self) -> bool:
        """Migrate existing JSON data to Supabase when ready"""
        if not self.use_supabase:
            self.logger.error("❌ Supabase not configured for migration")
            return False
        
        # TODO: Implement migration logic
        # 1. Read all JSON blueprints
        # 2. Convert to Supabase format
        # 3. Bulk insert to Supabase
        # 4. Verify data integrity
        # 5. Archive JSON files
        
        self.logger.info("🔄 JSON to Supabase migration (not yet implemented)")
        return True
    
    def backup_data(self) -> str:
        """Create backup of all data"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = self.data_dir / "backups" / f"backup_{timestamp}"
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        if self.use_supabase:
            # TODO: Implement Supabase backup
            self.logger.info(f"🔄 Supabase backup to {backup_dir} (not yet implemented)")
        else:
            # Backup JSON files
            import shutil
            try:
                # Copy blueprints
                blueprints_src = self.project_root / "content" / "blueprints"
                if blueprints_src.exists():
                    shutil.copytree(blueprints_src, backup_dir / "blueprints")
                
                # Copy data directory
                if self.data_dir.exists():
                    shutil.copytree(self.data_dir, backup_dir / "data")
                
                self.logger.info(f"💾 Backup created: {backup_dir}")
            except Exception as e:
                self.logger.error(f"❌ Backup failed: {e}")
                return ""
        
        return str(backup_dir)

# Global instance
_data_manager = None

def get_data_manager(use_supabase: bool = False) -> DataManager:
    """Get singleton data manager instance"""
    global _data_manager
    if _data_manager is None:
        _data_manager = DataManager(use_supabase=use_supabase)
    return _data_manager

# Test the data manager
if __name__ == "__main__":
    dm = DataManager()
    
    # Test blueprint operations
    test_blueprint = {
        "story_id": 99,
        "new": {
            "title": "Test Story",
            "genre": "Test Genre"
        },
        "generated_at": datetime.now().isoformat()
    }
    
    # Save and load test
    filepath = dm.save_blueprint(test_blueprint)
    loaded = dm.load_blueprint(99)
    blueprints = dm.list_blueprints()
    
    print(f"✅ Data manager test complete!")
    print(f"📁 Saved to: {filepath}")
    print(f"📋 Available blueprints: {len(blueprints)}")