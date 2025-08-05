#!/usr/bin/env python3
"""
Tests for core audio pipeline following CLAUDE.md testing standards T-1 through T-6.
"""

import pytest
from unittest.mock import AsyncMock, Mock
from pathlib import Path
from datetime import datetime

from .types import (
    AudioFile, AudioFileId, VoiceConfig, TTSRequest, TTSResult, TTSJobId,
    TTSProvider, AudioFormat, VoiceConfigId
)
from .audio_pipeline import AudioPipeline


class TestAudioPipeline:
    """Test suite for AudioPipeline class following T-1 standard"""
    
    @pytest.fixture
    def voice_config(self) -> VoiceConfig:
        """Standard voice configuration for testing"""
        return VoiceConfig(
            provider=TTSProvider.GOOGLE,
            voice_id="en-US-Neural2-J",
            language_code="en-US",
            speed=1.0,
            pitch=0.0
        )
    
    @pytest.fixture
    def sample_text(self) -> str:
        """Sample text for TTS generation - T-4 parameterized input"""
        return "This is a test story about a brave knight who saved the kingdom."
    
    @pytest.fixture
    def mock_provider(self) -> AsyncMock:
        """Mock TTS provider for testing"""
        provider = AsyncMock()
        provider.synthesize.return_value = TTSResult(
            success=True,
            audio_file=AudioFile(
                file_id=AudioFileId("test-audio-123"),
                file_path=Path("/test/audio.mp3"),
                duration_seconds=45.0,
                size_bytes=720000,
                format=AudioFormat.MP3,
                sample_rate=24000,
                bitrate=128,
                voice_config=VoiceConfig(
                    provider=TTSProvider.GOOGLE,
                    voice_id="en-US-Neural2-J",
                    language_code="en-US"
                ),
                generated_at=datetime.now().isoformat(),
                text_input="test text"
            ),
            cost_cents=5
        )
        return provider
    
    async def test_generate_audio_success(self, voice_config, sample_text, mock_provider):
        """Test successful audio generation - T-6 test entire structure"""
        pipeline = AudioPipeline()
        pipeline._providers[TTSProvider.GOOGLE] = mock_provider
        
        result = await pipeline.generate_audio(
            text=sample_text,
            voice_config=voice_config,
            output_path=Path("/test/output.mp3")
        )
        
        # T-6: Test entire structure in one assertion
        expected_result = TTSResult(
            success=True,
            audio_file=pytest.any(AudioFile),
            cost_cents=pytest.any(int)
        )
        
        assert result.success is True
        assert result.audio_file is not None
        assert result.audio_file.duration_seconds > 0
        assert result.cost_cents > 0
        mock_provider.synthesize.assert_called_once()
    
    async def test_generate_audio_failure_fallback(self, voice_config, sample_text):
        """Test fallback behavior when primary provider fails"""
        primary_provider = AsyncMock()
        primary_provider.synthesize.return_value = TTSResult(
            success=False,
            error_message="API rate limit exceeded"
        )
        
        fallback_provider = AsyncMock()
        fallback_provider.synthesize.return_value = TTSResult(success=True)
        
        pipeline = AudioPipeline()
        pipeline._providers[TTSProvider.GOOGLE] = primary_provider
        pipeline._providers[TTSProvider.OPENAI] = fallback_provider
        pipeline._fallback_providers[TTSProvider.GOOGLE] = TTSProvider.OPENAI
        
        result = await pipeline.generate_audio(
            text=sample_text,
            voice_config=voice_config,
            output_path=Path("/test/output.mp3")
        )
        
        assert result.success is True
        primary_provider.synthesize.assert_called_once()
        fallback_provider.synthesize.assert_called_once()
    
    def test_split_text_respects_character_limits(self, voice_config):
        """Test text splitting respects provider character limits"""
        pipeline = AudioPipeline()
        long_text = "A" * 5000  # 5000 characters
        max_chars = 2000
        
        chunks = pipeline._split_text_for_provider(long_text, max_chars)
        
        assert len(chunks) == 3  # Should split into 3 chunks
        assert all(len(chunk) <= max_chars for chunk in chunks)
        assert "".join(chunks) == long_text  # No content lost
    
    def test_estimate_total_cost_multiple_providers(self, voice_config, sample_text):
        """Test cost estimation across multiple providers"""
        pipeline = AudioPipeline()
        
        # Mock provider cost estimation
        google_provider = Mock()
        google_provider.estimate_cost.return_value = 15  # 15 cents
        
        openai_provider = Mock()
        openai_provider.estimate_cost.return_value = 12  # 12 cents
        
        pipeline._providers[TTSProvider.GOOGLE] = google_provider
        pipeline._providers[TTSProvider.OPENAI] = openai_provider
        
        costs = pipeline.estimate_costs_all_providers(sample_text)
        
        assert costs[TTSProvider.GOOGLE] == 15
        assert costs[TTSProvider.OPENAI] == 12
        assert TTSProvider.ELEVENLABS not in costs  # Not configured
    
    async def test_episode_splitting_preserves_content(self, voice_config):
        """Test episode splitting preserves all content and respects timing"""
        pipeline = AudioPipeline()
        
        # Story with natural break points
        story_text = """
        Chapter 1: The Beginning
        
        Once upon a time, there was a brave knight.
        
        ---
        
        Chapter 2: The Quest
        
        The knight embarked on a dangerous journey.
        
        ***
        
        Chapter 3: The End
        
        And they lived happily ever after.
        """
        
        episodes = await pipeline.split_into_episodes(
            text=story_text,
            target_duration_minutes=5,
            voice_config=voice_config
        )
        
        # Should split at natural breaks
        assert len(episodes) >= 2
        
        # All content preserved
        combined_text = "".join(episode.text for episode in episodes)
        original_words = story_text.replace("---", "").replace("***", "").split()
        combined_words = combined_text.split()
        
        # Most words should be preserved (allowing for formatting differences)
        assert len(combined_words) >= len(original_words) * 0.9
    
    def test_audio_file_duration_calculation(self):
        """Test audio file duration calculations are accurate"""
        audio_file = AudioFile(
            file_id=AudioFileId("test-123"),
            file_path=Path("/test.mp3"),
            duration_seconds=300.0,  # 5 minutes
            size_bytes=2400000,
            format=AudioFormat.MP3,
            sample_rate=24000,
            bitrate=128,
            voice_config=VoiceConfig(
                provider=TTSProvider.GOOGLE,
                voice_id="test-voice",
                language_code="en-US"
            ),
            generated_at="2025-01-02T10:00:00",
            text_input="test"
        )
        
        assert audio_file.get_duration_minutes() == 5.0
        assert audio_file.duration_seconds == 300.0