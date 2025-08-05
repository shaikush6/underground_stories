#!/usr/bin/env python3
"""
Tests for Fairer Tales adapter integration.
Following CLAUDE.md testing standards T-1 through T-6.
"""

import pytest
from unittest.mock import AsyncMock, Mock, patch
from pathlib import Path
from datetime import datetime

from .fairer_tales_adapter import FairerTalesAdapter, FairerTalesStory, FairerTalesEpisode
from ..core.audio.types import VoiceConfig, TTSProvider, AudioFormat, TTSResult, AudioFile


class TestFairerTalesAdapter:
    """Test suite for FairerTalesAdapter following T-1 standard"""
    
    @pytest.fixture
    def adapter(self):
        """Fairer Tales adapter instance for testing"""
        # Mock the story processor to avoid needing actual API calls
        with patch('packages.fairer-tales.fairer_tales_adapter.FlipsideProcessor'):
            adapter = FairerTalesAdapter()
            # Set test voice config
            adapter.voice_config = VoiceConfig(
                provider=TTSProvider.OPENAI,
                voice_id="ash",
                language_code="en-US",
                audio_format=AudioFormat.MP3
            )
            return adapter
    
    @pytest.fixture
    def sample_story_result(self):
        """Sample story generation result from existing system"""
        return {
            'success': True,
            'story_title': 'The Forest Therapist',
            'story_id': 'forest_therapist_001',
            'filepath': '/test/stories/forest_therapist.txt',
            'word_count': 2500,
            'style': 'sympathetic_antihero'
        }
    
    @pytest.fixture
    def sample_story_text(self):
        """Sample story text for testing episode splitting"""
        return """
        # The Forest Therapist
        *Dark Eco-Comedy / Woodland Noir*

        **Logline:** A misunderstood wolf-therapist must expose a poaching cartel run by Granny without breaking patient confidentiality or triggering a forest-wide relapse.

        ============================================================

        A panicked thump. The stag lurched sideways, hooves carving wet furrows in the moss. The therapy circle shattered for a heartbeat—rabbits pressed back into bracken, wings snapped taut, a dozen prey eyes fixed on the lone wolf at their center.

        Dr. Lupus Grimm did not flinch. Instead, he folded himself smaller, haunches sinking until his shoulders brushed the earth. His voice, low and steady, threaded through the hush.

        --- 

        Chapter 2: The Investigation

        The next morning brought devastating news. Three more animals had disappeared during the night, and the forest was in chaos. Dr. Grimm knew he had to act, but his oath of confidentiality bound him in ways that could cost lives.

        As he walked through the misty woods, the weight of his decisions pressed down like the fog itself. Every shadow could hide a threat, every sound could signal another disappearance.

        ---

        Chapter 3: The Confrontation

        The truth was worse than he had imagined. Granny's cottage sat at the center of a complex web of illegal hunting operations, and Red was just another victim, forced into compliance through threats to her family.

        Dr. Grimm stood at the edge of the clearing, knowing that his next choice would determine the fate of every creature in the forest. The therapeutic approach had its limits, and sometimes, protecting the vulnerable required more direct action.
        """
    
    @pytest.fixture
    def mock_audio_pipeline(self):
        """Mock audio pipeline for testing"""
        pipeline = AsyncMock()
        
        # Mock episode splitting
        pipeline.split_into_episodes.return_value = [
            Mock(text="Episode 1 content...", estimated_duration_minutes=4.5, sequence_number=1),
            Mock(text="Episode 2 content...", estimated_duration_minutes=5.2, sequence_number=2),
            Mock(text="Episode 3 content...", estimated_duration_minutes=4.8, sequence_number=3)
        ]
        
        # Mock audio generation
        pipeline.generate_audio.return_value = TTSResult(
            success=True,
            audio_file=AudioFile(
                file_id="test_audio_001",
                file_path=Path("/test/audio.mp3"),
                duration_seconds=270,  # 4.5 minutes
                size_bytes=2160000,
                format=AudioFormat.MP3,
                sample_rate=22050,
                bitrate=128,
                voice_config=VoiceConfig(
                    provider=TTSProvider.OPENAI,
                    voice_id="ash",
                    language_code="en-US"
                ),
                generated_at=datetime.now().isoformat(),
                text_input="test content"
            ),
            cost_cents=12
        )
        
        return pipeline
    
    def test_extract_story_metadata_correctly(self, adapter, sample_story_text, sample_story_result):
        """Test metadata extraction from generated story text"""
        metadata = adapter._extract_story_metadata(sample_story_text, sample_story_result)
        
        # T-6: Test entire structure in one assertion
        expected_metadata = {
            'title': 'The Forest Therapist',
            'genre': 'Dark Eco-Comedy / Woodland Noir', 
            'logline': pytest.any(str)
        }
        
        assert metadata['title'] == expected_metadata['title']
        assert metadata['genre'] == expected_metadata['genre']
        assert 'wolf-therapist' in metadata['logline']
    
    def test_clean_story_text_removes_metadata(self, adapter, sample_story_text):
        """Test story text cleaning removes headers and metadata"""
        clean_text = adapter._clean_story_text(sample_story_text)
        
        # Should not contain metadata markers
        assert '# The Forest Therapist' not in clean_text
        assert '**Logline:**' not in clean_text
        assert '=====' not in clean_text
        
        # Should contain actual story content
        assert 'Dr. Lupus Grimm' in clean_text
        assert 'panicked thump' in clean_text
    
    async def test_split_into_episodes_creates_proper_episodes(
        self, adapter, sample_story_text, mock_audio_pipeline
    ):
        """Test episode splitting creates properly structured episodes"""
        adapter.audio_pipeline = mock_audio_pipeline
        
        episodes = await adapter._split_into_episodes(
            story_text=sample_story_text,
            story_title="The Forest Therapist", 
            generate_audio=False
        )
        
        # Should create episodes
        assert len(episodes) > 0
        
        # Each episode should have required properties
        for episode in episodes:
            assert isinstance(episode, FairerTalesEpisode)
            assert episode.story_title == "The Forest Therapist"
            assert episode.episode_number > 0
            assert len(episode.text_content) > 0
            assert episode.estimated_duration_minutes > 0
            assert 'Episode' in episode.episode_title
    
    def test_generate_episode_title_creates_engaging_titles(self, adapter):
        """Test episode title generation creates engaging YouTube-friendly titles"""
        title = adapter._generate_episode_title(
            story_title="The Forest Therapist",
            episode_num=1,
            text="A panicked thump. The stag lurched sideways..."
        )
        
        assert "The Forest Therapist" in title
        assert "Episode 1" in title
        assert "The Beginning" in title  # Should use predefined engaging title
    
    async def test_generate_episode_audio_creates_audio_file(
        self, adapter, mock_audio_pipeline
    ):
        """Test audio generation for individual episodes"""
        adapter.audio_pipeline = mock_audio_pipeline
        
        episode = FairerTalesEpisode(
            story_title="Test Story",
            episode_number=1,
            episode_title="Test Episode",
            text_content="This is a test episode with some content for audio generation.",
            estimated_duration_minutes=5.0
        )
        
        audio_path = await adapter._generate_episode_audio(episode)
        
        assert audio_path is not None
        assert isinstance(audio_path, Path)
        assert audio_path.suffix == '.mp3'
        
        # Should call audio pipeline
        mock_audio_pipeline.generate_audio.assert_called_once()
    
    @patch('builtins.open')
    @patch('pathlib.Path.exists')
    async def test_generate_complete_story_integration(
        self, mock_exists, mock_open, adapter, sample_story_text, 
        sample_story_result, mock_audio_pipeline
    ):
        """Test complete story generation workflow integration"""
        # Setup mocks
        mock_exists.return_value = True
        mock_open.return_value.__enter__.return_value.read.return_value = sample_story_text
        
        adapter.story_processor.process_blueprint_text = AsyncMock(return_value=sample_story_result)
        adapter.audio_pipeline = mock_audio_pipeline
        
        # Test blueprint
        blueprint = """17 Forest Therapist — Dark Eco-Comedy / Woodland Noir
        
        Logline: A misunderstood wolf-therapist must expose a poaching cartel.
        
        | Character | Dr. Lupus Grimm, licensed eco-therapist |
        | Conflict  | Patient confidentiality vs. forest safety |
        | Setting   | Therapeutic forest clearing |
        | Theme     | Ethics vs. action, healing trauma |
        """
        
        story = await adapter.generate_complete_story(
            blueprint_text=blueprint,
            style="sympathetic_antihero",
            generate_audio=False
        )
        
        # T-6: Test entire structure in one assertion
        assert isinstance(story, FairerTalesStory)
        assert story.title == "The Forest Therapist"
        assert story.total_episodes > 0
        assert len(story.episodes) == story.total_episodes
        assert story.metadata['voice_config'] is not None
        
        # Should have called existing story processor
        adapter.story_processor.process_blueprint_text.assert_called_once()
    
    def test_get_available_styles_returns_pov_styles(self, adapter):
        """Test that available styles returns POV styles from existing system"""
        styles = adapter.get_available_styles()
        
        assert isinstance(styles, dict)
        assert len(styles) > 0
        
        # Should contain expected style keys
        expected_styles = ['sympathetic_antihero', 'social_commentary', 'psychological_thriller']
        available_keys = list(styles.keys())
        
        # At least some expected styles should be present
        assert any(style in available_keys for style in expected_styles)
    
    def test_voice_config_fallback_on_load_failure(self):
        """Test voice config falls back to defaults if loading fails"""
        # Create adapter with non-existent config file
        with patch('packages.fairer-tales.fairer_tales_adapter.FlipsideProcessor'):
            adapter = FairerTalesAdapter(voice_config_path="nonexistent.yml")
        
        # Should fall back to ash voice (your proven choice)
        assert adapter.voice_config.provider == TTSProvider.OPENAI
        assert adapter.voice_config.voice_id == "ash"
        assert adapter.voice_config.language_code == "en-US"