"""
The Flipside Configuration
==========================

Configuration settings for villain POV fairy tale transformation.
"""

# === PROCESSING SETTINGS ===
PROCESSING_CONFIG = {
    # Models to use for different tasks
    "models": {
        "modernization": "gpt-4",  # Primary modernization model
        "style_consistency": "gpt-4",  # Style harmonization
        "flow_optimization": "gpt-4",  # Reading flow enhancement
        "continuity_check": "gpt-4",  # Continuity and final polish
        "analysis": "gpt-4"  # Character and narrative analysis
    },
    
    # Temperature settings for different tasks
    "temperatures": {
        "modernization": 0.4,  # Balanced creativity and consistency
        "style_consistency": 0.2,  # Low for consistency
        "flow_optimization": 0.3,  # Moderate for natural flow
        "continuity_check": 0.2,  # Low for accuracy
        "analysis": 0.3  # Moderate for good analysis
    },
    
    # Processing options for villain POV transformation
    "options": {
        "villain_pov_focus": True,  # Transform to villain's perspective
        "sympathetic_portrayal": True,  # Make villain sympathetic/complex
        "modern_context": True,  # Add contemporary social issues
        "psychological_depth": True,  # Develop complex motivations
        "antihero_appeal": True,  # Create compelling antihero
        "subvert_expectations": True,  # Unexpected plot twists
        "short_story_structure": True,  # Optimize for short story format
        "preserve_fairy_tale_essence": True  # Keep recognizable fairy tale elements
    }
}

# === STYLE GUIDELINES ===
STYLE_GUIDELINES = {
    "narrative_voice": {
        "consistency": "Maintain consistent narrative perspective throughout",
        "tense": "Keep original tense unless clarity requires change",
        "formality": "Reduce excessive formality while maintaining literary quality"
    },
    
    "dialogue": {
        "naturalism": "Make dialogue sound natural to modern ears",
        "character_distinction": "Preserve unique character voice patterns",
        "period_awareness": "Keep period-appropriate vocabulary where it adds flavor"
    },
    
    "descriptions": {
        "clarity": "Enhance clarity without losing atmospheric quality",
        "pacing": "Adjust pacing for better reading flow",
        "imagery": "Preserve vivid imagery and literary devices"
    },
    
    "structure": {
        "paragraphs": "Optimize paragraph breaks for modern reading patterns",
        "transitions": "Smooth scene and topic transitions",
        "flow": "Ensure logical progression and natural rhythm"
    }
}

# === QUALITY STANDARDS ===
QUALITY_STANDARDS = {
    "readability": {
        "target_audience": "General adult readers",
        "complexity_level": "Accessible but literary",
        "sentence_variety": "Mix of short, medium, and longer sentences",
        "vocabulary_level": "Rich but not archaic"
    },
    
    "literary_preservation": {
        "original_meaning": "100% preservation required",
        "character_development": "All character arcs maintained",
        "plot_integrity": "Complete plot preservation",
        "thematic_elements": "Preserve themes and symbolism"
    },
    
    "modernization_goals": {
        "accessibility": "Make accessible to contemporary readers",
        "engagement": "Improve reading engagement and flow",
        "clarity": "Enhance clarity without oversimplification",
        "authenticity": "Maintain authentic period setting and atmosphere"
    }
}

# === CONTINUITY TRACKING ===
CONTINUITY_ELEMENTS = {
    "character_tracking": [
        "names_and_aliases",
        "personality_traits", 
        "speech_patterns",
        "relationships",
        "character_development_arcs"
    ],
    
    "plot_tracking": [
        "timeline_events",
        "location_changes",
        "important_objects",
        "mysteries_and_revelations",
        "conflicts_and_resolutions"
    ],
    
    "world_building": [
        "setting_descriptions",
        "cultural_elements",
        "technology_level",
        "social_structures",
        "geographical_features"
    ]
}

# === OUTPUT SETTINGS ===
OUTPUT_CONFIG = {
    "file_naming": {
        "individual_chapters": "chapter_{:02d}_modernized.txt",
        "full_book": "{book_title}_modernized_complete.txt",
        "metadata": "{book_title}_modernization_metadata.json",
        "style_guide": "{book_title}_style_guide.json"
    },
    
    "formatting": {
        "chapter_separator": "=" * 60,
        "chapter_header_template": "CHAPTER {chapter_num}",
        "encoding": "utf-8",
        "line_endings": "\n"
    },
    
    "metadata_tracking": {
        "processing_timestamp": True,
        "model_versions": True,
        "character_registry": True,
        "style_evolution": True,
        "quality_metrics": True
    }
}

# === FAIRY TALE SPECIFIC SETTINGS ===
# Configuration for The Flipside fairy tale collection
BOOK_CONFIGS = {
    "the_flipside": {
        "title": "The Flipside",
        "author": "Shai Kush", 
        "original_period": "Traditional Fairy Tales",
        "genre": "Villain POV Short Stories",
        "narrative_style": "First person (villain POV)",
        "target_audience": "Young Adult / Adult Crossover",
        "tone_options": [
            "psychological_thriller",
            "dark_comedy", 
            "sympathetic_antihero",
            "social_commentary",
            "modern_realism"
        ],
        "special_considerations": [
            "Transform villain into sympathetic protagonist",
            "Maintain fairy tale recognizability", 
            "Add psychological complexity",
            "Incorporate contemporary social issues",
            "Subvert reader expectations",
            "Short story pacing and structure",
            "Antihero appeal and moral ambiguity"
        ]
    },
    
    "default": {
        "title": "Custom Fairy Tale",
        "author": "Unknown", 
        "original_period": "Traditional",
        "genre": "POV Transformation",
        "narrative_style": "Variable",
        "special_considerations": [
            "POV transformation principles apply"
        ]
    }
}

# === VILLAIN POV PROCESSING STAGES ===
PROCESSING_STAGES = {
    "stage_1": {
        "name": "Fairy Tale Analysis",
        "description": "Analyze original fairy tale structure and characters",
        "agent": "FairytaleAnalyzer",
        "focus": "Understanding source material and villain role"
    },
    
    "stage_2": {
        "name": "POV Transformation", 
        "description": "Rewrite story from villain's perspective",
        "agent": "POVTransformer",
        "focus": "Shifting narrative perspective to villain"
    },
    
    "stage_3": {
        "name": "Psychological Development",
        "description": "Add psychological depth and sympathetic motivations",
        "agent": "PsychologyAgent", 
        "focus": "Complex character development and motivation"
    },
    
    "stage_4": {
        "name": "Modern Context Integration",
        "description": "Incorporate contemporary social issues and relevance",
        "agent": "ModernContextAgent",
        "focus": "Contemporary social commentary and relevance"
    },
    
    "stage_5": {
        "name": "Antihero Polish",
        "description": "Final polish for antihero appeal and narrative consistency",
        "agent": "AntiheroAgent",
        "focus": "Compelling antihero character and story completion"
    }
}

# === POV TRANSFORMATION STYLES ===
POV_STYLES = {
    "sympathetic_antihero": {
        "description": "Make villain relatable and sympathetic",
        "tone": "Understanding, complex, morally ambiguous",
        "techniques": ["Show hidden motivations", "Reveal circumstances", "Humanize decisions"]
    },
    
    "psychological_thriller": {
        "description": "Dark psychological exploration",
        "tone": "Intense, introspective, unsettling",
        "techniques": ["Internal monologue", "Psychological complexity", "Moral ambiguity"]
    },
    
    "dark_comedy": {
        "description": "Humorous take on villain's perspective", 
        "tone": "Witty, ironic, self-aware",
        "techniques": ["Ironic observations", "Self-deprecating humor", "Absurd situations"]
    },
    
    "social_commentary": {
        "description": "Use story to comment on social issues",
        "tone": "Thoughtful, critical, relevant",
        "techniques": ["Modern parallels", "System critique", "Social justice themes"]
    },
    
    "tragic_hero": {
        "description": "Villain as fallen hero or victim of circumstances",
        "tone": "Melancholic, regretful, noble",
        "techniques": ["Tragic backstory", "Noble intentions", "Unfortunate circumstances"]
    }
}