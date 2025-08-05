import React from 'react';
import { 
  AbsoluteFill, 
  Audio, 
  useCurrentFrame, 
  useVideoConfig,
  staticFile,
  interpolate,
  Easing
} from 'remotion';
import { VideoProps } from '../Root';
import { StaticImageDisplay } from './StaticImageDisplay';
import { UndergroundBranding } from './UndergroundBranding';
// Removed subtitle displays per user request - YouTube has built-in subtitles

export const UndergroundVideo: React.FC<VideoProps> = ({
  title,
  episode,
  pipeline,
  audioPath,
  duration
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  
  // Calculate progress (0 to 1) throughout the video
  const progress = interpolate(frame, [0, durationInFrames], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.linear
  });

  // Underground Stories color scheme
  const colors = {
    background: '#2C2C2C',    // Deep charcoal
    accent: '#B87333',        // Copper/rust
    text: '#F5F5F5',          // Off-white
    highlight: '#00BFFF',     // Electric blue
  };

  return (
    <AbsoluteFill>
      {/* Audio Track */}
      {audioPath && (
        <Audio src={staticFile(audioPath)} />
      )}
      
      {/* Background Layer */}
      <AbsoluteFill
        style={{
          background: `linear-gradient(135deg, ${colors.background} 0%, #1a1a1a 50%, ${colors.background} 100%)`,
        }}
      />
      
      {/* Underground Stories Branding - Top Bar */}
      <AbsoluteFill>
        <UndergroundBranding 
          title={title}
          episode={episode}
          pipeline={pipeline}
          progress={progress}
        />
      </AbsoluteFill>
      
      {/* Main Visual Area - Static Image Display */}
      <AbsoluteFill
        style={{
          top: 120,
          height: 740,
          padding: '20px 40px',
        }}
      >
        <StaticImageDisplay 
          progress={progress}
          imagePath="wolf_image_test.png"
          pipeline={pipeline}
        />
      </AbsoluteFill>
      
      {/* Text displays removed - YouTube provides built-in subtitles */}
      
      {/* Progress Bar - Bottom */}
      <AbsoluteFill
        style={{
          top: 1040,
          height: 40,
          padding: '10px 40px',
        }}
      >
        <div style={{
          width: '100%',
          height: '20px',
          backgroundColor: 'rgba(0, 0, 0, 0.3)',
          borderRadius: '10px',
          overflow: 'hidden',
        }}>
          <div
            style={{
              width: `${progress * 100}%`,
              height: '100%',
              background: `linear-gradient(90deg, ${colors.accent} 0%, ${colors.highlight} 100%)`,
              borderRadius: '10px',
              transition: 'width 0.1s ease-out',
            }}
          />
        </div>
        
        {/* Time Display */}
        <div style={{
          color: colors.text,
          fontSize: '14px',
          fontFamily: 'Arial, sans-serif',
          marginTop: '5px',
          textAlign: 'center',
        }}>
          {Math.floor((progress * duration) / 60)}:{String(Math.floor((progress * duration) % 60)).padStart(2, '0')} / {Math.floor(duration / 60)}:{String(duration % 60).padStart(2, '0')}
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
