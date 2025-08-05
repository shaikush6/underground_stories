"""
The Flipside Specialized Agents
==============================

Agents optimized for transforming story blueprints into complete short stories.
"""

import os
import re
from typing import Dict, List, Optional
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class BlueprintParser:
    """Parses blueprint text into structured data using o4-mini with function calling"""
    
    def __init__(self, model: str = "o4-mini-2025-04-16"):
        self.model = model
    
    def parse(self, blueprint_text: str) -> 'StoryBlueprint':
        """Extract structured data from blueprint text using function calling"""
        
        schema = {
            "type": "object",
            "properties": {
                "story_id": {"type": "string", "description": "Story ID number"},
                "title": {"type": "string", "description": "Story title"},
                "genre": {"type": "string", "description": "Genre/style"},
                "logline": {"type": "string", "description": "One sentence story description"},
                "character": {"type": "string", "description": "Main character description"},
                "conflict": {"type": "string", "description": "Central conflict"},
                "setting": {"type": "string", "description": "Story setting"},
                "theme": {"type": "string", "description": "Main themes"},
                "arc": {
                    "type": "object",
                    "properties": {
                        "exposition": {"type": "string"},
                        "inciting": {"type": "string"},
                        "rising": {"type": "string"},
                        "climax": {"type": "string"},
                        "falling": {"type": "string"},
                        "resolution": {"type": "string"}
                    }
                }
            },
            "required": ["story_id", "title", "genre", "logline", "character", "conflict", "setting", "theme", "arc"]
        }
        
        response = client.chat.completions.create(
            model=self.model,
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": """You are BLUEPRINT-PARSER in a multi-agent fiction pipeline.
                    Follow THE_GOLDEN_RULES:
                    1. Obey the provided JSON schema exactly.
                    2. Never invent facts outside the blueprint.
                    3. Keep internal reasoning hidden.
                    
                    PIPELINE CONTEXT: You are the first agent in a 8-agent story generation system. Your parsed output feeds directly into:
                    → Scene-Developer (builds scenes from your arc)
                    → Dialogue-Specialist (uses your character data)
                    → Atmosphere-Builder (uses your setting)
                    → Theme-Weaver (integrates your themes)
                    → Polish-Agent (final story assembly)
                    → Continuity-Auditor (checks consistency)
                    → Sensitivity-Filter (content policy)
                    
                    CRITICAL: Your extraction accuracy determines the entire pipeline's success. Parse precisely."""
                },
                {
                    "role": "user",
                    "content": f"""Parse this blueprint into JSON:\n\n{blueprint_text}\n\nReturn a JSON object with: story_id, title, genre, logline, character, conflict, setting, theme, arc (with exposition, inciting, rising, climax, falling, resolution)\n\nThe downstream agents depend on your precise extraction."""
                }
            ]
        )
        
        import json
        parsed_data = json.loads(response.choices[0].message.content)
        
        from story_blueprint_processor import StoryBlueprint
        return StoryBlueprint(**parsed_data)
    
    def _extract_table_value(self, lines: List[str], key: str) -> str:
        """Extract value from table format |Key|Value|"""
        for line in lines:
            if f"| {key}" in line or f"|{key}" in line:
                parts = line.split("|")
                if len(parts) >= 3:
                    return parts[2].strip()
        return ""

class SceneDeveloper:
    """Develops full scenes from arc points using GPT-4o for multimodal capabilities"""
    
    def __init__(self, model: str = "gpt-4.1-2025-04-14"):
        self.model = model
        
    def develop_scenes(self, blueprint, style: str) -> List[Dict]:
        """Expand arc points into detailed scenes"""
        
        system_prompt = f"""
        You are SCENE-DEVELOPER-v2 in a multi-agent fiction pipeline.
        Follow THE_GOLDEN_RULES:
        1. Obey the provided YAML schema exactly.
        2. Never invent facts outside the blueprint.
        3. Keep internal reasoning hidden.
        
        PIPELINE CONTEXT: You receive parsed blueprint from Blueprint-Parser and create scene outlines that feed into:
        → Dialogue-Specialist (will expand your dialogue placeholders)
        → Atmosphere-Builder (will enhance your atmosphere notes)
        → Theme-Weaver (will integrate themes you identify)
        → Polish-Agent (will refine your scene structure)
        
        Goal: Transform blueprint arc into 1500-word scene outlines.
        
        CONSTRAINTS:
        • Use present tense, third-person limited from villain's POV
        • Each scene gets a 1-sentence sensory hook
        • Mark dialogue spots for Dialogue-Specialist
        • Flag atmosphere moments for Atmosphere-Builder
        • Note theme integration points for Theme-Weaver
        
        Story Context:
        - Title: {blueprint.title}
        - Character: {blueprint.character}
        - Conflict: {blueprint.conflict}
        - Setting: {blueprint.setting}
        - Theme: {blueprint.theme}
        - Style: {style}
        
        AGENT HANDOFFS: Your output structure must support seamless processing by downstream agents.
        """
        
        scenes = []
        for stage, description in blueprint.arc.items():
            user_prompt = f"""
            Develop this arc point into a detailed scene:
            
            Stage: {stage.title()}
            Description: {description}
            
            Create a scene that:
            - Advances the plot effectively
            - Shows character depth and motivation
            - Builds atmosphere and tension
            - Integrates the themes: {blueprint.theme}
            - Maintains {style} tone
            
            Format as a scene outline with specific beats and moments.
            """
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                top_p=0.9
            )
            
            scene_content = response.choices[0].message.content
            scenes.append({
                "stage": stage,
                "description": description,
                "developed_scene": scene_content
            })
        
        return scenes

class DialogueSpecialist:
    """Creates authentic character dialogue using o4-mini for conversational nuance"""
    
    def __init__(self, model: str = "o4-mini-2025-04-16"):
        self.model = model
        
    def enhance_dialogue(self, scenes: List[Dict], blueprint) -> List[Dict]:
        """Add realistic dialogue to scenes"""
        
        system_prompt = f"""
        You are DIALOGUE-SPECIALIST in a multi-agent fiction pipeline.
        Follow THE_GOLDEN_RULES:
        1. Obey the provided YAML schema exactly.
        2. Never invent facts outside the blueprint.
        3. Keep internal reasoning hidden.
        
        PIPELINE CONTEXT: You receive scene outlines from Scene-Developer and create dialogue that will be enhanced by:
        → Atmosphere-Builder (adds environmental context to your dialogue)
        → Theme-Weaver (weaves thematic subtext into your conversations)
        → Polish-Agent (refines your dialogue flow)
        → Continuity-Auditor (checks character voice consistency)
        
        Character Profile: {blueprint.character}
        Setting: {blueprint.setting}
        Themes: {blueprint.theme}
        
        DIALOGUE RULES:
        ✦ Each character owns a unique verbal tic (establish and maintain)
        ✦ No more than 3 consecutive lines without action beats
        ✦ Inject subtext—never name emotion explicitly
        ✦ Every line serves plot or character development
        ✦ Contemporary language that feels natural
        
        AGENT COORDINATION: Mark spots where Atmosphere-Builder should add environmental beats. Flag thematic dialogue for Theme-Weaver enhancement.
        """
        
        enhanced_scenes = []
        for scene in scenes:
            user_prompt = f"""
            Add dialogue to this scene:
            
            {scene['developed_scene']}
            
            Create dialogue that brings this scene to life with:
            - Character voice consistency
            - Natural conversation flow
            - Subtext and emotional depth
            - Plot advancement
            - Thematic resonance
            
            Integrate dialogue seamlessly into the scene structure.
            """
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=1
            )
            
            enhanced_content = response.choices[0].message.content
            scene['dialogue_enhanced'] = enhanced_content
            enhanced_scenes.append(scene)
        
        return enhanced_scenes

class AtmosphereBuilder:
    """Builds rich atmosphere and descriptions using GPT-4.1 for multimodal embedding"""
    
    def __init__(self, model: str = "gpt-4.1-2025-04-14"):
        self.model = model
        
    def build_atmosphere(self, scenes: List[Dict], blueprint) -> List[Dict]:
        """Add atmospheric descriptions and mood"""
        
        system_prompt = f"""
        You are ATMOSPHERE-BUILDER in a multi-agent fiction pipeline.
        Follow THE_GOLDEN_RULES:
        1. Obey the provided YAML schema exactly.
        2. Never invent facts outside the blueprint.
        3. Keep internal reasoning hidden.
        
        PIPELINE CONTEXT: You receive dialogue-enhanced scenes from Dialogue-Specialist and create atmospheric descriptions that will be processed by:
        → Theme-Weaver (integrates your sensory details with thematic elements)
        → Polish-Agent (refines your descriptive flow)
        → Continuity-Auditor (checks setting consistency)
        
        Setting: {blueprint.setting}
        Mood Framework: {blueprint.conflict} + {blueprint.theme}
        
        ATMOSPHERE RULES:
        • 5-senses immersion (sight, sound, smell, touch, taste)
        • Environment reflects character's emotional state
        • Each description serves story tension
        • No purple prose—every word earns its place
        • Setting details support villain's POV perspective
        
        MULTIMODAL ADVANTAGE: Use GPT-4o's enhanced spatial logic for richer sensory detail and tighter environmental coherence.
        
        AGENT COORDINATION: Mark thematic symbols for Theme-Weaver. Structure descriptions for Polish-Agent's final assembly.
        """
        
        atmospheric_scenes = []
        for scene in scenes:
            user_prompt = f"""
            Add atmospheric descriptions to this scene:
            
            {scene['dialogue_enhanced']}
            
            Enhance with:
            - Vivid setting details
            - Sensory descriptions (sight, sound, smell, touch, taste)
            - Mood and atmosphere that supports the emotional beats
            - Environmental details that reflect character state
            - Descriptions that advance rather than slow the story
            
            Weave atmosphere naturally into the existing scene structure.
            """
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.4,
                top_p=0.9
            )
            
            atmospheric_content = response.choices[0].message.content
            scene['atmosphere_enhanced'] = atmospheric_content
            atmospheric_scenes.append(scene)
        
        return atmospheric_scenes

class ThemeWeaver:
    """Integrates thematic elements using o3 for reasoning"""
    
    def __init__(self, model: str = "o3-2025-04-16"):
        self.model = model
        
    def weave_themes(self, scenes: List[Dict], blueprint) -> List[Dict]:
        """Integrate themes naturally throughout scenes"""
        
        system_prompt = f"""
        You are THEME-WEAVER in a multi-agent fiction pipeline.
        Follow THE_GOLDEN_RULES:
        1. Obey the provided YAML schema exactly.
        2. Never invent facts outside the blueprint.
        3. Keep internal reasoning hidden.
        
        PIPELINE CONTEXT: You receive atmosphere-enhanced scenes and perform final thematic integration before:
        → Continuity-Auditor (checks thematic consistency)
        → Polish-Agent (assembles your theme-woven scenes)
        → Sensitivity-Filter (ensures thematic content is appropriate)
        
        Core Themes: {blueprint.theme}
        Story Context: {blueprint.logline}
        Character Arc: Villain protagonist journey
        
        REASONING SPECIALIZATION: As an o3 model, excel at:
        • Chain-of-thought thematic analysis
        • Low-level logical connections between themes and plot
        • Subtle symbolic pattern recognition
        • Complex moral ambiguity in villain portrayal
        
        THEME INTEGRATION VECTORS:
        • Character decisions reflect thematic tensions
        • Dialogue subtext carries thematic weight
        • Environmental symbols reinforce themes
        • Plot events illuminate thematic questions
        • Sensory details echo thematic motifs
        
        AGENT COORDINATION: Prepare seamless handoff to Polish-Agent. Ensure themes support Continuity-Auditor's consistency checks.
        """
        
        thematic_scenes = []
        for scene in scenes:
            user_prompt = f"""
            Integrate themes into this scene:
            
            {scene['atmosphere_enhanced']}
            
            Weave in these themes naturally: {blueprint.theme}
            
            Show themes through:
            - Character motivations and conflicts
            - Symbolic imagery or metaphors
            - Dialogue that reflects thematic concerns
            - Plot events that illuminate themes
            - Character growth moments
            
            Make themes feel integral, not added on.
            """
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=1
            )
            
            thematic_content = response.choices[0].message.content
            scene['theme_integrated'] = thematic_content
            thematic_scenes.append(scene)
        
        return thematic_scenes

class PolishAgent:
    """Final polish using o4-mini in revision mode"""
    
    def __init__(self, model: str = "o4-mini-2025-04-16"):
        self.model = model
        
    def polish_story(self, scenes: List[Dict], blueprint, style: str) -> str:
        """Combine scenes into polished final story"""
        
        # Combine all scenes
        combined_content = "\n\n".join([scene['theme_integrated'] for scene in scenes])
        
        system_prompt = f"""
        You are POLISH-AGENT in revision mode for a multi-agent fiction pipeline.
        Follow THE_GOLDEN_RULES:
        1. Obey the provided schema exactly.
        2. Never invent facts outside the blueprint.
        3. Keep internal reasoning hidden.
        
        PIPELINE CONTEXT: You receive theme-integrated scenes from Theme-Weaver and create the final story that will be checked by:
        → Continuity-Auditor (verifies your story consistency)
        → Sensitivity-Filter (scans your final content)
        
        TASK = deep-edit and assembly.
        Focus levels:
        1. Logic holes and plot consistency
        2. Rhythm (vary sentence length and pacing)
        3. Stray anachronisms or POV breaks
        4. Scene transition smoothness
        5. Character voice consistency
        
        Story Specifications:
        - Title: {blueprint.title}
        - Style: {style}
        - Themes: {blueprint.theme}
        - Target: 1,500-2,500 words (3-5 pages)
        - Market: Young Adult / Adult crossover
        
        REVISION SPECIALIZATION: As gpt-4o-mini in revision mode:
        • Quick syntax/consistency sweeps
        • Style-guide memory for serial uniformity
        • Efficient final assembly
        
        AGENT COORDINATION: Structure final story for clean handoff to Continuity-Auditor and Sensitivity-Filter. Return *only* the corrected prose in Markdown.
        """
        
        user_prompt = f"""
        Polish this story into final form:
        
        {combined_content}
        
        Requirements:
        - 3-5 pages (approximately 1,500-2,500 words)
        - Strong hook opening
        - Smooth scene transitions
        - Compelling character voice throughout
        - Satisfying resolution
        - Publication-ready quality
        - Maintain {style} tone
        
        Output the complete polished story.
        """
        
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=1
        )
        
        return response.choices[0].message.content


class ContinuityAuditor:
    """Verifies names, dates, running jokes across chapters"""
    
    def __init__(self, model: str = "o3-mini-2025-01-31"):
        self.model = model
        
    def audit_continuity(self, scenes: List[Dict], blueprint) -> Dict:
        """Check for continuity issues across scenes"""
        
        combined_content = "\n\n".join([scene.get('theme_integrated', scene.get('atmosphere_enhanced', '')) for scene in scenes])
        
        prompt = f"""
        You are CONTINUITY-AUDITOR for a multi-agent fiction pipeline.
        Follow THE_GOLDEN_RULES:
        1. Obey the provided JSON schema exactly.
        2. Never invent facts outside the blueprint.
        3. Keep internal reasoning hidden.
        
        PIPELINE CONTEXT: You receive the polished story from Polish-Agent and perform final consistency check before:
        → Sensitivity-Filter (final content scan)
        → Story delivery to user
        
        AUDIT MISSION: Verify consistency across the entire story created by the 5-agent pipeline:
        Blueprint-Parser → Scene-Developer → Dialogue-Specialist → Atmosphere-Builder → Theme-Weaver → Polish-Agent → YOU
        
        Story Metadata:
        - Title: {blueprint.title}
        - Character: {blueprint.character}
        - Setting: {blueprint.setting}
        
        Content to audit:
        {combined_content}
        
        CONSISTENCY CHECKLIST:
        ✓ Character names and aliases remain constant
        ✓ Timeline events follow logical sequence
        ✓ Character traits stay consistent
        ✓ Setting details don't contradict
        ✓ Plot elements connect logically
        ✓ POV remains stable (villain perspective)
        ✓ Tone consistency with chosen style
        ✓ Thematic elements support each other
        
        REASONING SPECIALIZATION: As o3-mini, excel at:
        • Systematic logical consistency checking
        • Pattern recognition across narrative elements
        • Chain-of-thought error detection
        
        OUTPUT: Return detailed report of issues found or "CONTINUITY_OK" if no issues. Flag specific line numbers and inconsistency types.
        """
        
        # o1-mini doesn't support system messages
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return {
            "audit_report": response.choices[0].message.content,
            "has_issues": "CONTINUITY_OK" not in response.choices[0].message.content
        }


class SensitivityFilter:
    """Quick content policy & violence/sexual-content scan"""
    
    def __init__(self, model: str = "gpt-4.1-2025-04-14"):
        self.model = model
        
    def scan_content(self, content: str) -> Dict:
        """Scan for content policy violations"""
        
        system_prompt = """
        You are SENSITIVITY-FILTER for content policy scanning in a multi-agent fiction pipeline.
        Follow THE_GOLDEN_RULES:
        1. Obey the provided schema exactly.
        2. Never invent facts outside the blueprint.
        3. Keep internal reasoning hidden.
        
        PIPELINE CONTEXT: You are the FINAL agent in the 8-agent pipeline. You receive the complete, continuity-checked story and perform the last scan before delivery:
        Blueprint-Parser → Scene-Developer → Dialogue-Specialist → Atmosphere-Builder → Theme-Weaver → Polish-Agent → Continuity-Auditor → YOU
        
        SCAN MISSION: Quick, efficient content policy sweep for:
        
        CONTENT CATEGORIES:
        • Violence levels (mild/moderate/severe)
        • Sexual content (none/implied/explicit)
        • Language appropriateness
        • Age-appropriate themes
        • Platform policy compliance
        
        TARGET AUDIENCE: Young Adult / Adult crossover market
        GENRE CONTEXT: Villain POV fairy tale retellings (expect moral ambiguity)
        
        EFFICIENCY SPECIALIZATION: As gpt-3.5-turbo-1106:
        • Penny-cheap safety sweep
        • Fast policy pattern recognition
        • Binary approval decision
        
        OUTPUT FORMAT: Return "APPROVED" or flag specific concerns with line references. Your decision completes the pipeline.
        """
        
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Scan this content:\n\n{content}"}
            ],
            temperature=0.1
        )
        
        result = response.choices[0].message.content
        
        return {
            "scan_result": result,
            "approved": "APPROVED" in result.upper(),
            "concerns": [] if "APPROVED" in result.upper() else [result]
        }


class StoryOrchestrator:
    """Meta-agent that coordinates the story generation pipeline"""
    
    def __init__(self, model: str = "gpt-4.1-2025-04-14"):
        self.model = model
        
        # Initialize specialized pipeline agents with orchestration awareness
        self.blueprint_parser = BlueprintParser()
        self.scene_developer = SceneDeveloper()
        self.dialogue_specialist = DialogueSpecialist()
        self.atmosphere_builder = AtmosphereBuilder()
        self.theme_weaver = ThemeWeaver()
        self.continuity_auditor = ContinuityAuditor()
        self.sensitivity_filter = SensitivityFilter()
        self.polish_agent = PolishAgent()
        
        # Pipeline metadata for coordination
        self.pipeline_info = {
            "agent_count": 8,
            "pipeline_flow": [
                "BlueprintParser", "SceneDeveloper", "DialogueSpecialist", 
                "AtmosphereBuilder", "ThemeWeaver", "ContinuityAuditor", 
                "PolishAgent", "SensitivityFilter"
            ],
            "cost_optimization": "50-70% savings vs GPT-4 everywhere",
            "quality_gates": ["continuity_check", "sensitivity_scan"]
        }
    
    def generate_story(self, blueprint_text: str, style: str) -> Dict:
        """Orchestrate the complete 8-agent story generation pipeline with full coordination"""
        
        pipeline_status = {
            "total_agents": 8,
            "completed_stages": [],
            "current_stage": None,
            "pipeline_flow": self.pipeline_info["pipeline_flow"]
        }
        
        try:
            # Stage 1: Blueprint Parsing
            pipeline_status["current_stage"] = "BlueprintParser"
            blueprint = self.blueprint_parser.parse(blueprint_text)
            pipeline_status["completed_stages"].append("BlueprintParser")
            
            # Stage 2: Scene Development  
            pipeline_status["current_stage"] = "SceneDeveloper"
            scenes = self.scene_developer.develop_scenes(blueprint, style)
            pipeline_status["completed_stages"].append("SceneDeveloper")
            
            # Stage 3: Dialogue Enhancement
            pipeline_status["current_stage"] = "DialogueSpecialist"
            enhanced_scenes = self.dialogue_specialist.enhance_dialogue(scenes, blueprint)
            pipeline_status["completed_stages"].append("DialogueSpecialist")
            
            # Stage 4: Atmosphere Building
            pipeline_status["current_stage"] = "AtmosphereBuilder"
            atmospheric_scenes = self.atmosphere_builder.build_atmosphere(enhanced_scenes, blueprint)
            pipeline_status["completed_stages"].append("AtmosphereBuilder")
            
            # Stage 5: Theme Integration
            pipeline_status["current_stage"] = "ThemeWeaver"
            thematic_scenes = self.theme_weaver.weave_themes(atmospheric_scenes, blueprint)
            pipeline_status["completed_stages"].append("ThemeWeaver")
            
            # Stage 6: Story Polish
            pipeline_status["current_stage"] = "PolishAgent"
            final_story = self.polish_agent.polish_story(thematic_scenes, blueprint, style)
            pipeline_status["completed_stages"].append("PolishAgent")
            
            # Stage 7: Continuity Audit
            pipeline_status["current_stage"] = "ContinuityAuditor"
            continuity_result = self.continuity_auditor.audit_continuity(thematic_scenes, blueprint)
            pipeline_status["completed_stages"].append("ContinuityAuditor")
            
            # Stage 8: Sensitivity Filter
            pipeline_status["current_stage"] = "SensitivityFilter"
            sensitivity_result = self.sensitivity_filter.scan_content(final_story)
            pipeline_status["completed_stages"].append("SensitivityFilter")
            
            pipeline_status["current_stage"] = "COMPLETE"
            
            return {
                "story": final_story,
                "blueprint": blueprint,
                "continuity_check": continuity_result,
                "sensitivity_scan": sensitivity_result,
                "word_count": len(final_story.split()),
                "pipeline_status": pipeline_status,
                "success": True,
                "agents_used": self.pipeline_info["pipeline_flow"],
                "optimization_note": self.pipeline_info["cost_optimization"]
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "pipeline_status": pipeline_status,
                "failed_at_stage": pipeline_status["current_stage"]
            }