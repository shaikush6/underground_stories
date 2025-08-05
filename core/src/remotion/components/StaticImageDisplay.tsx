import React from 'react';
import { interpolate, Easing, staticFile } from 'remotion';

interface StaticImageDisplayProps {
  progress: number; // 0 to 1
  imagePath: string;
  pipeline: 'fairer-tales' | 'timeless-retold' | 'minute-myths';
}

export const StaticImageDisplay: React.FC<StaticImageDisplayProps> = ({
  progress,
  imagePath,
  pipeline
}) => {
  
  // Underground Stories color palette
  const colors = {
    background: '#2C2C2C',
    accent: '#B87333',
    highlight: '#00BFFF',
  };

  // Slow, elegant fade-in over first 3 seconds (assuming 30fps)
  const fadeInDuration = 0.05; // 5% of total video duration for fade-in
  const imageOpacity = interpolate(progress, [0, fadeInDuration], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.out(Easing.cubic)
  });

  // Subtle scale effect - starts slightly larger and settles
  const imageScale = interpolate(progress, [0, fadeInDuration * 2], [1.02, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.out(Easing.quad)
  });

  // Very subtle brightness adjustment for atmosphere
  const brightness = interpolate(progress, [0, fadeInDuration], [0.9, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp'
  });

  return (
    <div style={{ 
      width: '100%', 
      height: '100%', 
      position: 'relative',
      overflow: 'hidden',
      backgroundColor: colors.background
    }}>
      {/* Main static image */}
      <div
        style={{
          width: '100%',
          height: '100%',
          position: 'relative',
          transform: `scale(${imageScale})`,
          transition: 'transform 0.1s ease-out'
        }}
      >
        <img
          src={staticFile(imagePath)}
          alt="Episode artwork"
          style={{
            width: '100%',
            height: '100%',
            objectFit: 'cover', // Fill the 16:9 frame completely
            objectPosition: 'center',
            opacity: imageOpacity,
            filter: `brightness(${brightness})`,
            transition: 'opacity 0.1s ease-out, filter 0.1s ease-out'
          }}
        />
        
        {/* Subtle atmospheric overlay */}
        <div
          style={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            background: `linear-gradient(135deg, 
              rgba(44, 44, 44, 0.1) 0%, 
              transparent 40%, 
              transparent 60%, 
              rgba(0, 191, 255, 0.03) 100%)`,
            opacity: imageOpacity * 0.7,
            pointerEvents: 'none'
          }}
        />
      </div>

      {/* Optional: Subtle vignette effect for cinematic feel */}
      <div
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: `radial-gradient(circle at center, 
            transparent 30%, 
            rgba(0, 0, 0, 0.1) 70%, 
            rgba(0, 0, 0, 0.2) 100%)`,
          opacity: imageOpacity * 0.5,
          pointerEvents: 'none'
        }}
      />
    </div>
  );
};