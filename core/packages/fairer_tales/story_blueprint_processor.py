#!/usr/bin/env python3
"""
The Flipside Story Blueprint Processor
=====================================

Transforms detailed story blueprints into complete short stories using specialized agents.
"""

import os
import json
import time
from typing import Dict, List, Optional
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass

from .my_agents.writer_centric_agents import (
    BlueprintParser,
    WriterAgent,
    CharacterConsultant,
    ThemeConsultant,
    AtmosphereConsultant,
    ContinuityAuditor,
    StoryOrchestrator
)

from .modernization_config import BOOK_CONFIGS, POV_STYLES

# KDP Integration (optional, graceful degradation)
try:
    from kdp_automation import kdp_hook_story_generated, get_kdp_integration
    KDP_INTEGRATION_AVAILABLE = True
except ImportError:
    KDP_INTEGRATION_AVAILABLE = False
    def kdp_hook_story_generated(result): return result
    def get_kdp_integration(): return None

@dataclass
class StoryBlueprint:
    """Structure for enhanced story blueprint data"""
    story_id: str
    title: str
    genre: str
    logline: str
    character: str
    conflict: str
    setting: str
    theme: str
    arc: Dict[str, str]
    original_story_context: Optional[Dict] = None
    expanded_details: Optional[Dict] = None

class FlipsideProcessor:
    """
    Complete story generation from blueprints
    """
    
    def __init__(self):
        self.config = BOOK_CONFIGS["the_flipside"]
        self.output_dir = Path("output/stories")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize specialized agents
        self._init_agents()
        
        print("🔄 The Flipside Story Processor initialized")
        print(f"📁 Output directory: {self.output_dir}")

    def _init_agents(self):
        """Initialize Writer-Centric story generation architecture"""
        # Use the new Writer-Centric orchestrator
        self.orchestrator = StoryOrchestrator()
        
        # Access Writer-Centric components
        self.blueprint_parser = self.orchestrator.blueprint_parser
        self.writer_agent = self.orchestrator.writer_agent
        self.continuity_auditor = self.orchestrator.continuity_auditor
        
        # Access consultant agents through writer
        self.character_consultant = self.writer_agent.character_consultant
        self.theme_consultant = self.writer_agent.theme_consultant
        self.atmosphere_consultant = self.writer_agent.atmosphere_consultant
        
        print("🎭 Writer-Centric story generation architecture initialized")
        print("✍️ Master Writer Agent ready with Hemingway-level precision")

    def parse_blueprint(self, blueprint_text: str) -> StoryBlueprint:
        """Parse blueprint text into structured data"""
        return self.blueprint_parser.parse(blueprint_text)

    def generate_story(self, blueprint: StoryBlueprint, style: str = "sympathetic_antihero") -> str:
        """
        Generate complete story using Writer-Centric architecture
        
        Args:
            blueprint: Structured story blueprint
            style: POV style from POV_STYLES config
            
        Returns:
            Complete short story text
        """
        print(f"🎭 Writer-Centric Generation: {blueprint.title}")
        print("✍️ Master Writer Agent with consultant guidance...")
        
        # Writer-Centric Process: Writer Agent with Consultant Guidance
        story_result = self.writer_agent.write_complete_story(blueprint, style)
        
        print(f"📊 Story Stats:")
        print(f"   • Scenes: {story_result['scenes_count']}")
        print(f"   • Words: {story_result['word_count']}")
        print(f"   • Architecture: Writer-Centric with 3 Consultants")
        
        print(f"✅ Story complete: {blueprint.title}")
        return story_result["story"]

    def save_story(self, story_text: str, blueprint: StoryBlueprint) -> str:
        """Save generated story to file"""
        filename = f"{blueprint.story_id}_{blueprint.title.lower().replace(' ', '_')}.txt"
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"# {blueprint.title}\n")
            f.write(f"*{blueprint.genre}*\n\n")
            f.write(f"**Logline:** {blueprint.logline}\n\n")
            f.write("=" * 60 + "\n\n")
            f.write(story_text)
        
        print(f"💾 Story saved: {filepath}")
        return str(filepath)

    def process_blueprint_text(self, blueprint_text: str, style: str = "sympathetic_antihero") -> Dict:
        """Complete pipeline: blueprint text -> finished story using optimized orchestrator"""
        try:
            # Use optimized orchestrator
            result = self.orchestrator.generate_story(blueprint_text, style)
            
            if result["success"]:
                # Save story
                filepath = self.save_story(result["story"], result["blueprint"])
                
                # Prepare enhanced result
                enhanced_result = {
                    "success": True,
                    "story_title": result["blueprint"].title,
                    "story_id": result["blueprint"].story_id,
                    "filepath": filepath,
                    "word_count": result["word_count"],
                    "style": style,
                    "continuity_check": result["continuity_check"],
                    "sensitivity_scan": result["sensitivity_scan"],
                    "architecture": result.get("architecture", "Writer-Centric"),
                    "pipeline_status": result.get("pipeline_status", {}),
                    "optimization_note": result.get("optimization_note", "")
                }
                
                # KDP Integration Hook (safe - returns unchanged result if disabled)
                enhanced_result = kdp_hook_story_generated(enhanced_result)
                
                return enhanced_result
            else:
                return result
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

# Example usage
if __name__ == "__main__":
    # Test with Green Card story
    green_card_blueprint = """
17 Green Card — Dark Fantasy / Witness-Protection Parable

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
    6.    Resolution: International tribunal grants frogs (now human) political asylum; Mirella vanishes into deeper bog, new portal glowing.
"""
    
    processor = FlipsideProcessor()
    result = processor.process_blueprint_text(green_card_blueprint, "social_commentary")
    print(f"\n🎉 Processing result: {result}")