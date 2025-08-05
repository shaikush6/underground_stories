import React from 'react';
import { interpolate, Easing, staticFile } from 'remotion';

interface ProgressiveImageRevealProps {
  progress: number; // 0 to 1
  imagePath: string;
  pipeline: 'fairer-tales' | 'timeless-retold' | 'minute-myths';
  drawingStyle?: 'pencil' | 'brush' | 'pen';
}

export const ProgressiveImageReveal: React.FC<ProgressiveImageRevealProps> = ({
  progress,
  imagePath,
  pipeline,
  drawingStyle = 'brush'
}) => {
  
  // Underground Stories color palette
  const colors = {
    primary: '#B87333',      // Copper
    secondary: '#00BFFF',    // Electric blue  
    accent: '#F5F5F5',       // Off-white
  };

  // Calculate reveal area - we'll reveal from top-left to bottom-right in a natural drawing pattern
  const revealProgress = interpolate(progress, [0, 1], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
    easing: Easing.out(Easing.cubic)
  });

  // Create a circular reveal mask that grows over time
  const maskRadius = interpolate(revealProgress, [0, 1], [0, 1400], {
    easing: Easing.out(Easing.quad)
  });

  // Drawing cursor position - follows a natural path
  const cursorPath = [
    // Start from top-left area (wolf's head)
    { x: 0.3, y: 0.2, stage: 0.0 },
    // Move to eyes and face details
    { x: 0.45, y: 0.25, stage: 0.2 },
    // Down to body and chair
    { x: 0.5, y: 0.5, stage: 0.4 },
    // Lamp and environment
    { x: 0.7, y: 0.3, stage: 0.6 },
    // Final details and shadows
    { x: 0.6, y: 0.8, stage: 0.8 },
    // Complete
    { x: 0.5, y: 0.5, stage: 1.0 }
  ];

  // Find current cursor position
  const getCurrentCursorPos = () => {
    for (let i = 0; i < cursorPath.length - 1; i++) {
      const current = cursorPath[i];
      const next = cursorPath[i + 1];
      
      if (revealProgress >= current.stage && revealProgress <= next.stage) {
        const segmentProgress = interpolate(
          revealProgress,
          [current.stage, next.stage],
          [0, 1]
        );
        
        return {
          x: interpolate(segmentProgress, [0, 1], [current.x, next.x]) * 1920,
          y: interpolate(segmentProgress, [0, 1], [current.y, next.y]) * 1080
        };
      }
    }
    
    // Fallback to last position
    const last = cursorPath[cursorPath.length - 1];
    return { x: last.x * 1920, y: last.y * 1080 };
  };

  const cursorPos = getCurrentCursorPos();

  // Drawing cursor styles
  const cursorStyles = {
    pencil: {
      size: 8,
      color: '#2B2B2B',
      opacity: 0.8,
      trail: true
    },
    brush: {
      size: 12,
      color: colors.primary,
      opacity: 0.7,
      trail: true
    },
    pen: {
      size: 6,
      color: '#1A1A1A',
      opacity: 0.9,
      trail: false
    }
  };

  const currentCursorStyle = cursorStyles[drawingStyle];

  // Show cursor only when actively revealing (not at start or end)
  const showCursor = revealProgress > 0.02 && revealProgress < 0.98;

  return (
    <div style={{ 
      width: '100%', 
      height: '100%', 
      position: 'relative',
      overflow: 'hidden'
    }}>
      {/* Base image with progressive reveal mask */}
      <div
        style={{
          width: '100%',
          height: '100%',
          position: 'relative',
        }}
      >
        {/* The actual image */}
        <img
          src={staticFile(imagePath)}
          alt="Progressive reveal artwork"
          style={{
            width: '100%',
            height: '100%',
            objectFit: 'contain',
            clipPath: `circle(${maskRadius}px at ${cursorPos.x}px ${cursorPos.y}px)`,
            transition: 'clip-path 0.1s ease-out'
          }}
        />
        
        {/* Subtle overlay for atmosphere */}
        <div
          style={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            background: `linear-gradient(135deg, rgba(44, 44, 44, 0.1) 0%, transparent 50%, rgba(0, 191, 255, 0.05) 100%)`,
            pointerEvents: 'none',
            clipPath: `circle(${maskRadius}px at ${cursorPos.x}px ${cursorPos.y}px)`,
            transition: 'clip-path 0.1s ease-out'
          }}
        />
      </div>

      {/* Drawing cursor */}
      {showCursor && (
        <div
          style={{
            position: 'absolute',
            left: cursorPos.x - currentCursorStyle.size,
            top: cursorPos.y - currentCursorStyle.size,
            width: currentCursorStyle.size * 2,
            height: currentCursorStyle.size * 2,
            borderRadius: '50%',
            backgroundColor: currentCursorStyle.color,
            opacity: currentCursorStyle.opacity,
            boxShadow: `0 0 ${currentCursorStyle.size}px rgba(0, 0, 0, 0.3)`,
            pointerEvents: 'none',
            zIndex: 10,
            transform: 'translate(-50%, -50%)',
            transition: 'all 0.1s ease-out'
          }}
        />
      )}

      {/* Drawing trail effect (optional) */}
      {showCursor && currentCursorStyle.trail && (
        <div
          style={{
            position: 'absolute',
            left: cursorPos.x - (currentCursorStyle.size * 0.7),
            top: cursorPos.y - (currentCursorStyle.size * 0.7),
            width: currentCursorStyle.size * 1.4,
            height: currentCursorStyle.size * 1.4,
            borderRadius: '50%',
            backgroundColor: currentCursorStyle.color,
            opacity: currentCursorStyle.opacity * 0.3,
            pointerEvents: 'none',
            zIndex: 9,
            transform: 'translate(-50%, -50%)',
            transition: 'all 0.15s ease-out'
          }}
        />
      )}

      {/* Progress indicator */}
      <div
        style={{
          position: 'absolute',
          bottom: 20,
          right: 20,
          color: colors.accent,
          fontSize: '14px',
          fontFamily: 'Arial, sans-serif',
          opacity: 0.7,
          textShadow: '1px 1px 2px rgba(0, 0, 0, 0.8)'
        }}
      >
        Drawing: {Math.round(revealProgress * 100)}%
      </div>
    </div>
  );
};