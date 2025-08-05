#!/usr/bin/env python3
"""
Intelligent Text Chunker for TTS Providers
==========================================

Splits long text into provider-safe chunks while preserving narrative flow.
Handles sentence boundaries, dialogue, and dramatic pauses intelligently.
"""

import re
from typing import List, Tuple
from dataclasses import dataclass
from pathlib import Path


@dataclass
class TextChunk:
    """A chunk of text optimized for TTS generation"""
    text: str
    chunk_index: int
    total_chunks: int
    character_count: int
    estimated_duration_seconds: float
    chunk_type: str = "narrative"  # narrative, dialogue, transition
    
    def __post_init__(self):
        # Calculate estimated duration (average 150 words per minute)
        word_count = len(self.text.split())
        self.estimated_duration_seconds = (word_count / 150) * 60


class IntelligentTextChunker:
    """
    Smart text chunking that preserves narrative flow and dramatic timing.
    
    Features:
    - Respects sentence boundaries
    - Preserves dialogue integrity
    - Maintains dramatic pauses
    - Optimizes for TTS provider limits
    - Handles different content types (stories, dialogue, narration)
    """
    
    def __init__(self, max_chars: int = 4000, overlap_chars: int = 100):
        """
        Initialize chunker with provider-specific limits.
        
        Args:
            max_chars: Maximum characters per chunk (4000 for OpenAI safety margin)
            overlap_chars: Character overlap between chunks for smooth transitions
        """
        self.max_chars = max_chars
        self.overlap_chars = overlap_chars
        
        # Sentence boundary patterns (sophisticated for story content)
        self.sentence_patterns = [
            r'(?<=[.!?])\s+(?=[A-Z])',  # Standard sentence endings
            r'(?<=[.!?]")\s+(?=[A-Z])',  # Quoted sentence endings
            r'(?<=[.!?])\s+(?="[A-Z])',  # Start of quoted dialogue
            r'(?<=\.)\s*\n\s*(?=[A-Z])',  # Paragraph breaks
            r'(?<=[.!?])\s+(?=—)',  # Em-dash transitions
        ]
        
        # Dialogue and dramatic pause patterns
        self.dialogue_patterns = [
            r'"[^"]*"',  # Quoted dialogue
            r'—[^—]*—',  # Em-dash enclosed thoughts
            r'\*[^*]*\*',  # Action descriptions
        ]
        
        # Natural break points (in order of preference)
        self.break_patterns = [
            r'\n\n+',  # Paragraph breaks (highest priority)
            r'(?<=[.!?])\s*\n',  # Sentence + line break
            r'(?<=[.!?])\s+(?=[A-Z])',  # Sentence boundaries
            r'(?<=,)\s+(?=And |But |However |Meanwhile |Then |Now |Still )',  # Transition words
            r'(?<=;)\s+',  # Semicolon breaks
            r'(?<=:)\s+',  # Colon breaks
            r'(?<=,)\s+',  # Comma breaks (last resort)
        ]
    
    def chunk_text(self, text: str, content_type: str = "story") -> List[TextChunk]:
        """
        Split text into intelligent chunks optimized for TTS.
        
        Args:
            text: The text to chunk
            content_type: Type of content (story, dialogue, narration)
            
        Returns:
            List of TextChunk objects ready for TTS processing
        """
        # Clean and normalize text
        text = self._normalize_text(text)
        
        if len(text) <= self.max_chars:
            return [TextChunk(
                text=text,
                chunk_index=1,
                total_chunks=1,
                character_count=len(text),
                estimated_duration_seconds=0,  # Will be calculated in __post_init__
                chunk_type=content_type
            )]
        
        # Find optimal split points
        chunks = self._split_intelligently(text)
        
        # Create TextChunk objects
        text_chunks = []
        total_chunks = len(chunks)
        
        for i, chunk_text in enumerate(chunks):
            chunk = TextChunk(
                text=chunk_text.strip(),
                chunk_index=i + 1,
                total_chunks=total_chunks,
                character_count=len(chunk_text),
                estimated_duration_seconds=0,  # Calculated in __post_init__
                chunk_type=self._detect_chunk_type(chunk_text)
            )
            text_chunks.append(chunk)
        
        return text_chunks
    
    def _normalize_text(self, text: str) -> str:
        """Clean and normalize text for optimal TTS processing"""
        # Remove excessive whitespace
        text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)  # Max 2 line breaks
        text = re.sub(r' +', ' ', text)  # Remove multiple spaces
        text = text.strip()
        
        # Ensure proper spacing around punctuation
        text = re.sub(r'([.!?])([A-Z])', r'\1 \2', text)
        
        # Fix common TTS issues
        text = re.sub(r'—', ' — ', text)  # Space around em-dashes
        text = re.sub(r'  +', ' ', text)  # Clean up double spaces
        
        return text
    
    def _split_intelligently(self, text: str) -> List[str]:
        """Split text using intelligent break points"""
        chunks = []
        remaining_text = text
        
        while remaining_text:
            if len(remaining_text) <= self.max_chars:
                chunks.append(remaining_text)
                break
            
            # Find the best split point within the character limit
            split_point = self._find_optimal_split(remaining_text)
            
            if split_point == -1:
                # Force split at character limit if no good break point found
                split_point = self.max_chars
                # Try to avoid splitting mid-word
                while split_point > 0 and remaining_text[split_point] not in [' ', '\n', '\t']:
                    split_point -= 1
                if split_point == 0:
                    split_point = self.max_chars
            
            # Extract chunk with potential overlap for smooth transitions
            chunk = remaining_text[:split_point].strip()
            chunks.append(chunk)
            
            # Move to next chunk with overlap consideration
            next_start = max(split_point - self.overlap_chars, split_point)
            remaining_text = remaining_text[next_start:].strip()
        
        return chunks
    
    def _find_optimal_split(self, text: str) -> int:
        """Find the best place to split text within character limits"""
        # Search for break patterns in order of preference
        for pattern in self.break_patterns:
            matches = list(re.finditer(pattern, text[:self.max_chars]))
            if matches:
                # Use the last match within the limit (longest possible chunk)
                return matches[-1].end()
        
        return -1  # No good break point found
    
    def _detect_chunk_type(self, text: str) -> str:
        """Detect the type of content in a chunk for TTS optimization"""
        # Count dialogue vs narrative
        dialogue_matches = len(re.findall(r'"[^"]*"', text))
        total_sentences = len(re.findall(r'[.!?]', text))
        
        if dialogue_matches > total_sentences * 0.5:
            return "dialogue"
        elif re.search(r'(Meanwhile|Then|Now|Later|Suddenly)', text):
            return "transition"
        else:
            return "narrative"
    
    def get_chunking_stats(self, chunks: List[TextChunk]) -> dict:
        """Get statistics about the chunking results"""
        total_chars = sum(chunk.character_count for chunk in chunks)
        total_duration = sum(chunk.estimated_duration_seconds for chunk in chunks)
        
        return {
            "total_chunks": len(chunks),
            "total_characters": total_chars,
            "total_estimated_duration_minutes": total_duration / 60,
            "average_chunk_size": total_chars / len(chunks) if chunks else 0,
            "largest_chunk": max(chunk.character_count for chunk in chunks) if chunks else 0,
            "smallest_chunk": min(chunk.character_count for chunk in chunks) if chunks else 0,
            "chunk_types": {chunk_type: len([c for c in chunks if c.chunk_type == chunk_type]) 
                           for chunk_type in ["narrative", "dialogue", "transition"]}
        }


# Utility functions for integration
def chunk_story_episode(episode_text: str) -> List[TextChunk]:
    """Convenience function to chunk a story episode"""
    chunker = IntelligentTextChunker(max_chars=4000, overlap_chars=100)
    return chunker.chunk_text(episode_text, content_type="story")


def chunk_for_provider(text: str, provider: str) -> List[TextChunk]:
    """Chunk text based on specific TTS provider limits"""
    limits = {
        "openai": 4000,  # Conservative limit for OpenAI TTS
        "google": 5000,  # Google Cloud TTS limit
        "elevenlabs": 2500,  # ElevenLabs standard limit
    }
    
    max_chars = limits.get(provider.lower(), 4000)
    chunker = IntelligentTextChunker(max_chars=max_chars)
    return chunker.chunk_text(text)


if __name__ == "__main__":
    # Test the chunker with sample text
    sample_text = """
    Dr. Lupus Grimm sat in his forest sanctuary, surrounded by woodland creatures who had once fled from his kind. The therapy circle was an unlikely gathering: rabbits, deer, birds, and even a nervous squirrel—all seeking healing from past traumas.
    
    "Today, we practice the breathing technique," Grimm said softly, his voice deliberately gentle. "Remember, fear is normal. But we can choose how we respond to it."
    
    A young rabbit trembled. "What if the hunters come back?"
    
    Grimm's eyes softened. "Then we'll face that fear together. But right now, in this moment, you are safe."
    """
    
    chunker = IntelligentTextChunker()
    chunks = chunker.chunk_text(sample_text)
    stats = chunker.get_chunking_stats(chunks)
    
    print(f"Chunked into {len(chunks)} parts:")
    for chunk in chunks:
        print(f"\nChunk {chunk.chunk_index}/{chunk.total_chunks} ({chunk.chunk_type}):")
        print(f"Characters: {chunk.character_count}")
        print(f"Duration: {chunk.estimated_duration_seconds:.1f}s")
        print(f"Text: {chunk.text[:100]}...")
    
    print(f"\nStats: {stats}")