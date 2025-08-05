import React from 'react';
import { interpolate, Easing } from 'remotion';

interface PartSpecificTextDisplayProps {
  progress: number; // 0 to 1
  pipeline: 'fairer-tales' | 'timeless-retold' | 'minute-myths';
  storyTitle: string;
  duration: number; // Total video duration in seconds
  part: number; // 1, 2, or 3
}

export const PartSpecificTextDisplay: React.FC<PartSpecificTextDisplayProps> = ({
  progress,
  pipeline,
  storyTitle,
  duration,
  part
}) => {
  
  const colors = {
    background: '#2C2C2C',
    accent: '#B87333',
    text: '#F5F5F5',
    highlight: '#00BFFF',
  };

  // Part-specific story segments with proper timing for each 5-minute segment
  const getPartSegments = (partNumber: number) => {
    const allSegments = {
      1: [
        { start: 0, end: 25, text: "Dr. Lupus Grimm sat in his forest sanctuary, surrounded by woodland creatures who had once fled from his kind. The therapy circle was an unlikely gathering." },
        { start: 25, end: 55, text: "Years of anger management and healing work had transformed the legendary Big Bad Wolf into something unprecedented: a forest therapist." },
        { start: 55, end: 85, text: "But when corporate developers threatened to destroy his sanctuary, his peaceful nature would be tested like never before." },
        { start: 85, end: 115, text: "The animals looked to him with eyes full of hope and fear - would their healer become their protector?" },
        { start: 115, end: 145, text: "Dr. Grimm closed his eyes and felt the old rage stirring. This time, however, it would serve a different purpose." },
        { start: 145, end: 175, text: "Sometimes healing others means first healing the world around them. Sometimes a villain's greatest redemption is knowing when to fight." },
        { start: 175, end: 205, text: "The forest sanctuary had become more than a therapy space - it was home to dozens of creatures seeking peace." },
        { start: 205, end: 235, text: "As bulldozers approached the tree line, Dr. Grimm made a choice that would define his true character..." },
        { start: 235, end: 265, text: "The morning mist carried the scent of diesel and destruction. Time was running out for the sanctuary." },
        { start: 265, end: 301, text: "Dr. Grimm gathered his patients for what might be their final therapy session together..." }
      ],
      2: [
        { start: 0, end: 30, text: "The corporate executives had underestimated the bond between the wolf and his woodland patients." },
        { start: 30, end: 60, text: "Using his therapy skills, Dr. Grimm organized the animals not for battle, but for strategic negotiation." },
        { start: 60, end: 90, text: "The forest echoed with unified voices - prey and predator standing together for their shared home." },
        { start: 90, end: 120, text: "Media attention grew as the story spread: a reformed villain protecting those he once terrorized." },
        { start: 120, end: 150, text: "Dr. Grimm realized this confrontation would test every healing technique he had learned." },
        { start: 150, end: 180, text: "The animals watched their therapist transform into their advocate, their protector, their leader." },
        { start: 180, end: 210, text: "Legal challenges arose, environmental groups rallied, and the sanctuary became a symbol of redemption." },
        { start: 210, end: 240, text: "But the developers had one final card to play - a card that would test Dr. Grimm's resolve completely." },
        { start: 240, end: 270, text: "As negotiations reached a breaking point, the old wolf felt his carefully controlled anger rising..." },
        { start: 270, end: 301, text: "The moment of truth approached - would healing triumph over destruction?" }
      ],
      3: [
        { start: 0, end: 30, text: "As the final confrontation began, Dr. Grimm realized this was his greatest therapy session yet." },
        { start: 30, end: 60, text: "The developers' lawyers arrived with eviction notices, but they hadn't expected an army of forest creatures." },
        { start: 60, end: 90, text: "Dr. Grimm's greatest lesson emerged: sometimes protecting others requires embracing your true nature." },
        { start: 90, end: 120, text: "The Big Bad Wolf howled once more - not in anger, but in triumph and protection." },
        { start: 120, end: 150, text: "Media coverage turned the sanctuary into a national symbol of environmental protection and redemption." },
        { start: 150, end: 180, text: "The corporate retreat marked more than a victory - it was proof that even villains can find their path to heroism." },
        { start: 180, end: 210, text: "Dr. Grimm's therapy circle expanded, welcoming both creatures and humans seeking healing." },
        { start: 210, end: 240, text: "The forest sanctuary became a protected space, a testament to the power of transformation and community." },
        { start: 240, end: 270, text: "Years later, Dr. Lupus Grimm would reflect on the day he learned that sometimes healing requires fighting..." },
        { start: 270, end: 301, text: "And sometimes, the greatest redemption comes from protecting those who once feared you." }
      ]
    };
    return allSegments[partNumber] || [];
  };

  const storySegments = getPartSegments(part);
  
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
          {storyTitle} Part {part} • {Math.floor(currentTime / 60)}:{String(Math.floor(currentTime % 60)).padStart(2, '0')}
        </div>
      </div>
    </div>
  );
};
