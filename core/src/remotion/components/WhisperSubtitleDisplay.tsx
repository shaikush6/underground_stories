import React from 'react';
import { interpolate, Easing } from 'remotion';

interface WhisperSubtitleDisplayProps {
  progress: number; // 0 to 1
  pipeline: 'fairer-tales' | 'timeless-retold' | 'minute-myths';
  storyTitle: string;
  duration: number; // Total video duration in seconds
  part: number; // 1, 2, or 3
  audioPath: string; // Audio filename for subtitle lookup
}

export const WhisperSubtitleDisplay: React.FC<WhisperSubtitleDisplayProps> = ({
  progress,
  pipeline,
  storyTitle,
  duration,
  part,
  audioPath
}) => {
  
  const colors = {
    background: '#2C2C2C',
    accent: '#B87333',
    text: '#F5F5F5',
    highlight: '#00BFFF',
  };

  // Load subtitle data - from Whisper-generated JSON files or fallback to demo
  const getSubtitleData = (audioFilename: string) => {
    // Try to load from generated subtitle file first
    try {
      // For now, use embedded demo subtitles that match the Huff & Heal story
      // TODO: Load from /content/subtitles/[audiofile]_subtitles.json when available
      if (audioFilename.includes('Huff_and_Heal') || audioFilename.includes('Huff') || audioFilename.includes('Heal')) {
        return [
          {"text": "Dr. Lupus Grimm sat in his forest sanctuary, surrounded by woodland creatures who had once fled from his kind.", "start": 0.0, "end": 8.5},
          {"text": "The therapy circle was an unlikely gathering - rabbits beside the wolf who once chased them,", "start": 8.5, "end": 15.2},
          {"text": "birds perched fearlessly on branches above the predator who once hunted them.", "start": 15.2, "end": 21.8},
          {"text": "Years of anger management and healing work had transformed the legendary Big Bad Wolf", "start": 21.8, "end": 28.5},
          {"text": "into something unprecedented: a forest therapist.", "start": 28.5, "end": 33.2},
          {"text": "But when corporate developers threatened to destroy his sanctuary,", "start": 33.2, "end": 38.9},
          {"text": "his peaceful nature would be tested like never before.", "start": 38.9, "end": 44.6},
          {"text": "The animals looked to him with eyes full of hope and fear -", "start": 44.6, "end": 50.3},
          {"text": "would their healer become their protector?", "start": 50.3, "end": 55.0},
          {"text": "Dr. Grimm closed his eyes and felt the old rage stirring.", "start": 55.0, "end": 61.7},
          {"text": "This time, however, it would serve a different purpose.", "start": 61.7, "end": 67.4},
          {"text": "Sometimes healing others means first healing the world around them.", "start": 67.4, "end": 74.1},
          {"text": "Sometimes a villain's greatest redemption is knowing when to fight.", "start": 74.1, "end": 80.8},
          {"text": "The forest sanctuary had become more than a therapy space -", "start": 80.8, "end": 86.5},
          {"text": "it was home to dozens of creatures seeking peace.", "start": 86.5, "end": 92.2},
          {"text": "As bulldozers approached the tree line,", "start": 92.2, "end": 96.9},
          {"text": "Dr. Grimm made a choice that would define his true character.", "start": 96.9, "end": 103.6},
          {"text": "The morning mist carried the scent of diesel and destruction.", "start": 103.6, "end": 109.3},
          {"text": "Time was running out for the sanctuary.", "start": 109.3, "end": 114.0},
          {"text": "Dr. Grimm gathered his patients for what might be their final therapy session together.", "start": 114.0, "end": 122.7},
          {"text": "But this session would be different.", "start": 122.7, "end": 127.4},
          {"text": "This session would determine not just their healing,", "start": 127.4, "end": 133.1},
          {"text": "but their very survival.", "start": 133.1, "end": 137.8},
          {"text": "The reformed wolf was about to discover", "start": 137.8, "end": 142.5},
          {"text": "that sometimes the greatest act of healing", "start": 142.5, "end": 147.2},
          {"text": "is knowing when to bare your teeth again.", "start": 147.2, "end": 152.9},
          {"text": "And in the distance, the sound of approaching machinery", "start": 152.9, "end": 158.6},
          {"text": "mixed with the determined howl of a wolf", "start": 158.6, "end": 163.3},
          {"text": "who had finally found something worth fighting for.", "start": 163.3, "end": 169.0},
          {"text": "The story of Dr. Lupus Grimm was about to enter", "start": 169.0, "end": 174.7},
          {"text": "its most challenging chapter yet.", "start": 174.7, "end": 180.0}
        ];
      }
    } catch (error) {
      console.log(`Error loading subtitle file for ${audioFilename}:`, error);
    }
    
    // Return null for other audio files (no subtitles)
    console.log(`No subtitle data available for ${audioFilename}`);
    return null;
  };

  const subtitleSegments = getSubtitleData(audioPath);
  
  // Find current subtitle segment based on video progress
  const currentTime = progress * duration;
  const currentSegment = subtitleSegments?.find(segment => 
    currentTime >= segment.start && currentTime < segment.end
  );

  // Calculate text fade in/out for smooth transitions
  const getTextOpacity = (segment: any) => {
    if (!segment) return 0;
    
    const segmentProgress = interpolate(
      currentTime,
      [segment.start, segment.start + 0.5, segment.end - 0.5, segment.end],
      [0, 1, 1, 0],
      {
        extrapolateLeft: 'clamp',
        extrapolateRight: 'clamp',
        easing: Easing.inOut(Easing.ease)
      }
    );
    return segmentProgress;
  };

  // Get pipeline-specific styling
  const pipelineStyles = {
    'fairer-tales': {
      fontSize: '22px',
      lineHeight: '1.4',
      fontWeight: 'normal',
    },
    'timeless-retold': {
      fontSize: '20px',
      lineHeight: '1.5',
      fontWeight: 'normal',
    },
    'minute-myths': {
      fontSize: '24px',
      lineHeight: '1.3',
      fontWeight: 'bold',
    }
  };

  const currentPipelineStyle = pipelineStyles[pipeline];

  // If no subtitles available, show nothing
  if (!subtitleSegments || !currentSegment) {
    return null;
  }

  return (
    <div
      style={{
        width: '100%',
        height: '100%',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        position: 'relative',
      }}
    >
      {/* Background overlay for text readability */}
      <div
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: `linear-gradient(180deg, transparent 0%, ${colors.background}aa 20%, ${colors.background}dd 50%, ${colors.background}aa 80%, transparent 100%)`,
          borderRadius: '15px',
        }}
      />

      {/* Whisper-generated subtitle text */}
      <div
        style={{
          maxWidth: '1400px',
          textAlign: 'center',
          padding: '20px 40px',
          position: 'relative',
          zIndex: 1,
        }}
      >
        <p
          style={{
            color: colors.text,
            fontSize: currentPipelineStyle.fontSize,
            lineHeight: currentPipelineStyle.lineHeight,
            fontWeight: currentPipelineStyle.fontWeight,
            fontFamily: 'Arial, sans-serif',
            margin: 0,
            textShadow: '2px 2px 4px rgba(0, 0, 0, 0.8)',
            opacity: getTextOpacity(currentSegment),
            transition: 'opacity 0.3s ease-in-out',
          }}
        >
          {currentSegment.text}
        </p>

        {/* Story progress indicator with Whisper badge */}
        <div
          style={{
            position: 'absolute',
            bottom: '-40px',
            left: '50%',
            transform: 'translateX(-50%)',
            color: colors.accent,
            fontSize: '12px',
            fontFamily: 'Arial, sans-serif',
            opacity: 0.6,
            fontStyle: 'italic',
          }}
        >
          {storyTitle} Part {part} • Whisper AI Subtitles • {Math.floor(currentTime / 60)}:{String(Math.floor(currentTime % 60)).padStart(2, '0')}
        </div>
      </div>
    </div>
  );
};
