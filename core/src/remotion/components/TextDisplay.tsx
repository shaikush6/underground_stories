import React from 'react';
import { interpolate, Easing } from 'remotion';

interface TextDisplayProps {
  progress: number;
  pipeline: 'fairer-tales' | 'timeless-retold' | 'minute-myths';
  storyTitle: string;
}

export const TextDisplay: React.FC<TextDisplayProps> = ({
  progress,
  pipeline,
  storyTitle
}) => {
  
  const colors = {
    background: '#2C2C2C',
    accent: '#B87333',
    text: '#F5F5F5',
    highlight: '#00BFFF',
  };

  // Sample text segments for "Huff & Heal" - these would typically come from props or external data
  const textSegments = [
    {
      start: 0.0,
      end: 0.08,
      text: "Dr. Lupus Grimm sat in his forest sanctuary, surrounded by woodland creatures who had once fled from his kind."
    },
    {
      start: 0.08,
      end: 0.16,
      text: "The therapy circle was an unlikely gathering - rabbits, squirrels, and foxes learning to trust the reformed Big Bad Wolf."
    },
    {
      start: 0.16,
      end: 0.24,
      text: "Years of anger management and healing work had transformed the legendary villain into something unprecedented: a therapist."
    },
    {
      start: 0.24,
      end: 0.32,
      text: "But when corporate developers threatened to destroy the forest, his peaceful nature would be tested like never before."
    },
    {
      start: 0.32,
      end: 0.40,
      text: "The animals looked to him with eyes full of hope and fear - would their healer become their protector?"
    },
    {
      start: 0.40,
      end: 0.48,
      text: "Dr. Grimm closed his eyes and felt the old rage stirring. This time, however, it would serve a different purpose."
    },
    {
      start: 0.48,
      end: 0.56,
      text: "Sometimes healing others means first healing the world around them. Sometimes a villain's greatest redemption is knowing when to fight."
    },
    {
      start: 0.56,
      end: 0.64,
      text: "The forest sanctuary had become more than a therapy space - it was home to dozens of creatures seeking peace."
    },
    {
      start: 0.64,
      end: 0.72,
      text: "As bulldozers approached the tree line, Dr. Grimm made a choice that would define his true character."
    },
    {
      start: 0.72,
      end: 0.80,
      text: "He would not huff and puff to destroy. This time, he would huff and puff to heal, to protect, to preserve."
    },
    {
      start: 0.80,
      end: 0.88,
      text: "The Big Bad Wolf was dead. In his place stood something far more dangerous: a protector with nothing left to lose."
    },
    {
      start: 0.88,
      end: 0.96,
      text: "And so began the greatest therapy session of his career - teaching a world how to coexist with nature once again."
    },
    {
      start: 0.96,
      end: 1.0,
      text: "Sometimes the most powerful healing happens when we learn to channel our deepest nature toward love instead of destruction."
    }
  ];

  // Find current text segment
  const currentSegment = textSegments.find(segment => 
    progress >= segment.start && progress < segment.end
  );

  // Calculate text fade in/out
  const getTextOpacity = (segment: typeof textSegments[0]) => {
    const segmentProgress = interpolate(
      progress,
      [segment.start, segment.start + 0.01, segment.end - 0.01, segment.end],
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
      fontSize: '24px',
      lineHeight: '1.4',
      fontWeight: 'normal',
    },
    'timeless-retold': {
      fontSize: '22px',
      lineHeight: '1.5',
      fontWeight: 'normal',
    },
    'minute-myths': {
      fontSize: '26px',
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
          background: `linear-gradient(180deg, transparent 0%, ${colors.background}88 20%, ${colors.background}cc 50%, ${colors.background}88 80%, transparent 100%)`,
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
              transition: 'opacity 0.3s ease-in-out',
            }}
          >
            {currentSegment.text}
          </p>
        )}

        {/* Subtle story title reminder */}
        <div
          style={{
            position: 'absolute',
            bottom: '-30px',
            left: '50%',
            transform: 'translateX(-50%)',
            color: colors.accent,
            fontSize: '14px',
            fontFamily: 'Arial, sans-serif',
            opacity: 0.6,
            fontStyle: 'italic',
          }}
        >
          {storyTitle}
        </div>
      </div>
    </div>
  );
};