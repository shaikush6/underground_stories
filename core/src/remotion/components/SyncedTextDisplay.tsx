import React from 'react';
import { interpolate, Easing } from 'remotion';

interface SyncedTextDisplayProps {
  progress: number; // 0 to 1
  pipeline: 'fairer-tales' | 'timeless-retold' | 'minute-myths';
  storyTitle: string;
  duration: number; // Total video duration in seconds
}

export const SyncedTextDisplay: React.FC<SyncedTextDisplayProps> = ({
  progress,
  pipeline,
  storyTitle,
  duration
}) => {
  
  const colors = {
    background: '#2C2C2C',
    accent: '#B87333',
    text: '#F5F5F5',
    highlight: '#00BFFF',
  };

  // For now, we'll use steady scrolling text that matches the story pace
  // TODO: Replace with Whisper-generated precise timestamps
  
  // Sample story text segments for Huff & Heal with approximate timing
  const storySegments = [
    {
      start: 0,
      end: 20,
      text: "Dr. Lupus Grimm sat in his forest sanctuary, surrounded by woodland creatures who had once fled from his kind. The therapy circle was an unlikely gathering."
    },
    {
      start: 20,
      end: 45,
      text: "Years of anger management and healing work had transformed the legendary Big Bad Wolf into something unprecedented: a forest therapist."
    },
    {
      start: 45,
      end: 70,
      text: "But when corporate developers threatened to destroy his sanctuary, his peaceful nature would be tested like never before."
    },
    {
      start: 70,
      end: 95,
      text: "The animals looked to him with eyes full of hope and fear - would their healer become their protector?"
    },
    {
      start: 95,
      end: 120,
      text: "Dr. Grimm closed his eyes and felt the old rage stirring. This time, however, it would serve a different purpose."
    },
    {
      start: 120,
      end: 145,
      text: "Sometimes healing others means first healing the world around them. Sometimes a villain's greatest redemption is knowing when to fight."
    },
    {
      start: 145,
      end: 170,
      text: "The forest sanctuary had become more than a therapy space - it was home to dozens of creatures seeking peace."
    },
    {
      start: 170,
      end: 180,
      text: "As bulldozers approached the tree line, Dr. Grimm made a choice that would define his true character..."
    }
  ];

  // Find current text segment based on video progress
  const currentTime = progress * duration;
  const currentSegment = storySegments.find(segment => 
    currentTime >= segment.start && currentTime < segment.end
  );

  // Calculate text fade in/out for smooth transitions
  const getTextOpacity = (segment: typeof storySegments[0]) => {
    const segmentProgress = interpolate(
      currentTime,
      [segment.start, segment.start + 2, segment.end - 2, segment.end],
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

      {/* Text content */}
      <div
        style={{
          maxWidth: '1400px',
          textAlign: 'center',
          padding: '20px 40px',
          position: 'relative',
          zIndex: 1,
        }}
      >
        {currentSegment && (
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
              transition: 'opacity 0.5s ease-in-out',
            }}
          >
            {currentSegment.text}
          </p>
        )}

        {/* Story progress indicator */}
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
          {storyTitle} • {Math.floor(currentTime / 60)}:{String(Math.floor(currentTime % 60)).padStart(2, '0')}
        </div>
      </div>
    </div>
  );
};