"""
Enhanced Text Processing Agents
===============================

Advanced agents for sophisticated text modernization with focus on:
- Literary quality preservation
- Style consistency  
- Language flow optimization
- Character voice maintenance
- Narrative continuity
"""

import os
from typing import Dict, List, Optional
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class LiteraryModernizer:
    """Advanced literary modernization with style preservation"""
    
    def __init__(self, model: str = "gpt-4"):
        self.model = model
        
    def modernize_prose(self, text: str, context: Dict = None) -> str:
        """
        Modernize archaic text while preserving literary quality and voice
        """
        context_str = ""
        if context:
            if context.get("narrative_voice"):
                context_str += f"Narrative voice: {context['narrative_voice']}\n"
            if context.get("period"):
                context_str += f"Historical period: {context['period']}\n"
            if context.get("character_voices"):
                context_str += f"Character voices established: {context['character_voices']}\n"
        
        system_prompt = f"""
        You are a master literary editor specializing in modernizing classic literature for contemporary audiences while preserving the essence and artistry of the original work.

        Your expertise includes:
        - Classical and modern literature analysis
        - Language evolution and stylistic adaptation  
        - Character voice preservation across time periods
        - Narrative flow optimization
        - Cultural context sensitivity

        Guidelines for modernization:

        PRESERVE:
        - Core meaning and emotional impact
        - Character personalities and distinct voices
        - Narrative perspective and voice
        - Historical setting and atmosphere
        - Literary devices and stylistic flourishes that enhance the story
        - Dialogue authenticity within character parameters

        MODERNIZE:
        - Archaic vocabulary (thee, thou, hath, etc.)
        - Overly complex sentence structures that impede reading flow
        - Outdated expressions and idioms
        - Awkward passive voice constructions
        - Unnecessarily formal register in informal contexts

        ENHANCE:
        - Reading flow and pacing
        - Clarity without oversimplification
        - Natural dialogue rhythms
        - Paragraph transitions
        - Scene connectivity

        Context for this text:
        {context_str}

        Return only the modernized text with no commentary or explanations.
        """
        
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ],
            temperature=0.4
        )
        
        return response.choices[0].message.content.strip()

class StyleConsistencyAgent:
    """Ensures stylistic consistency across chapters"""
    
    def __init__(self, model: str = "gpt-4"):
        self.model = model
        
    def harmonize_style(self, text: str, style_guide: Dict, previous_context: List[str] = None) -> str:
        """
        Ensure stylistic consistency with established patterns
        """
        context_str = ""
        if style_guide:
            context_str += f"Established style guidelines:\n"
            for key, value in style_guide.items():
                context_str += f"- {key}: {value}\n"
        
        if previous_context:
            context_str += f"\nPrevious chapters context (last 3):\n"
            for i, summary in enumerate(previous_context[-3:], 1):
                context_str += f"{i}. {summary}\n"
        
        system_prompt = f"""
        You are a professional copy editor specializing in maintaining stylistic consistency across long-form narrative works.

        Your task is to review and refine this chapter text to ensure it aligns with the established style guidelines and maintains consistency with previous chapters.

        Focus areas:
        - Consistent use of vocabulary and terminology
        - Character voice consistency
        - Narrative tone consistency  
        - Punctuation and formatting standards
        - Transition smoothness between scenes
        - Paragraph structure optimization

        {context_str}

        Make subtle refinements to improve consistency while preserving the quality and flow of the modernized prose.

        Return only the refined text.
        """
        
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ],
            temperature=0.2
        )
        
        return response.choices[0].message.content.strip()

class FlowOptimizer:
    """Optimizes language flow and reading experience"""
    
    def __init__(self, model: str = "gpt-4"):
        self.model = model
        
    def optimize_flow(self, text: str, target_audience: str = "general adult") -> str:
        """
        Optimize text for natural reading flow and pacing
        """
        system_prompt = f"""
        You are an expert prose editor specializing in reading flow optimization and narrative pacing.

        Your task is to enhance this text for optimal reading experience while maintaining all content and literary quality.

        Target audience: {target_audience}

        Optimization focus:
        
        SENTENCE STRUCTURE:
        - Vary sentence lengths for rhythm and engagement
        - Break up overly long, complex sentences
        - Combine choppy short sentences where appropriate
        - Ensure logical flow between sentences

        PARAGRAPH FLOW:
        - Smooth transitions between paragraphs
        - Logical information progression
        - Appropriate paragraph breaks for pacing
        - Clear topic transitions

        READING EXPERIENCE:
        - Natural breathing points in dialogue
        - Effective use of punctuation for pacing
        - Clear antecedent relationships
        - Elimination of awkward phrasings

        PACING:
        - Action sequences: shorter, punchier sentences
        - Descriptive passages: flowing, rhythmic prose
        - Dialogue: natural speech patterns
        - Tension building: strategic sentence variation

        Maintain all plot points, character development, and narrative content while enhancing readability.

        Return only the optimized text.
        """
        
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ],
            temperature=0.3
        )
        
        return response.choices[0].message.content.strip()

class ContinuityChecker:
    """Ensures narrative and character continuity across chapters"""
    
    def __init__(self, model: str = "gpt-4"):
        self.model = model
        
    def check_continuity(self, text: str, continuity_context: Dict) -> str:
        """
        Check and correct continuity issues while polishing the text
        """
        context_str = ""
        if continuity_context.get("characters"):
            context_str += "Established characters:\n"
            for name, traits in continuity_context["characters"].items():
                context_str += f"- {name}: {traits}\n"
        
        if continuity_context.get("plot_points"):
            context_str += f"\nKey plot points from previous chapters:\n"
            for point in continuity_context["plot_points"]:
                context_str += f"- {point}\n"
        
        if continuity_context.get("world_building"):
            context_str += f"\nWorld building elements:\n"
            for element in continuity_context["world_building"]:
                context_str += f"- {element}\n"
        
        system_prompt = f"""
        You are a continuity editor responsible for ensuring narrative consistency across a multi-chapter work.

        Your task is to review this chapter for any continuity issues and make subtle corrections while performing a final polish.

        Continuity context from previous chapters:
        {context_str}

        Check for and correct:
        - Character name consistency and spelling
        - Character behavior consistency with established personalities
        - Plot element consistency with previous chapters
        - Setting and world-building consistency
        - Timeline consistency
        - Terminology consistency (especially proper nouns, technical terms)

        Final polish focus:
        - Grammar and punctuation refinement
        - Word choice optimization
        - Clarity improvements
        - Flow enhancements

        Make only necessary changes to maintain continuity and improve quality. Preserve the voice and style of the modernized text.

        Return only the final polished text.
        """
        
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ],
            temperature=0.2
        )
        
        return response.choices[0].message.content.strip()

class CharacterVoiceAnalyzer:
    """Analyzes and maintains character voice consistency"""
    
    def __init__(self, model: str = "gpt-4"):
        self.model = model
        
    def extract_character_voices(self, text: str) -> Dict[str, str]:
        """
        Extract character speech patterns and personality traits
        """
        system_prompt = """
        You are a character analysis expert. Analyze this text and extract character voices and personalities.

        For each character that speaks or is prominently featured, identify:
        - Speech patterns and vocabulary preferences
        - Personality traits evident in dialogue and actions
        - Relationship dynamics with other characters
        - Any distinctive verbal or behavioral quirks

        Return a JSON object where each character name is a key and the value is a concise description of their voice and key traits.

        Example format:
        {
            "Character Name": "Speech pattern description, key personality traits, distinctive features"
        }
        """
        
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ],
            temperature=0.3
        )
        
        try:
            import json
            return json.loads(response.choices[0].message.content)
        except:
            return {}

class QualityAssuranceAgent:
    """Final quality assurance and polish"""
    
    def __init__(self, model: str = "gpt-4"):
        self.model = model
        
    def final_quality_check(self, text: str) -> str:
        """
        Perform final quality assurance and polish
        """
        system_prompt = """
        You are a senior editor performing a final quality assurance review on modernized literary text.

        Perform a comprehensive final check:

        LANGUAGE QUALITY:
        - Grammar and punctuation accuracy
        - Word choice precision and appropriateness
        - Sentence structure effectiveness
        - Paragraph organization

        READABILITY:
        - Natural flow and rhythm
        - Clear antecedents and references
        - Logical progression of ideas
        - Appropriate pacing

        CONSISTENCY:
        - Internal consistency within the chapter
        - Consistent tone and voice
        - Character voice consistency
        - Style consistency

        LITERARY MERIT:
        - Preservation of original literary quality
        - Effective use of literary devices
        - Emotional impact retention
        - Narrative engagement

        Make only necessary refinements to achieve publication-quality prose while preserving the modernized style and content.

        Return only the final polished text.
        """
        
        response = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ],
            temperature=0.1
        )
        
        return response.choices[0].message.content.strip()