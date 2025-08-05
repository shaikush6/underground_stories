import React from 'react';
import { interpolate } from 'remotion';

interface UndergroundBrandingProps {
  title: string;
  episode: number;
  pipeline: 'fairer-tales' | 'timeless-retold' | 'minute-myths';
  progress: number;
}

export const UndergroundBranding: React.FC<UndergroundBrandingProps> = ({
  title,
  episode,
  pipeline,
  progress
}) => {
  
  const colors = {
    background: '#2C2C2C',
    accent: '#B87333',
    text: '#F5F5F5',
    highlight: '#00BFFF',
  };

  // Pipeline-specific styling
  const pipelineStyles = {
    'fairer-tales': {
      color: colors.accent,
      badge: 'FAIRER TALES',
      icon: '🧚'
    },
    'timeless-retold': {
      color: '#8b4513',
      badge: 'TIMELESS RETOLD',
      icon: '📚'
    },
    'minute-myths': {
      color: colors.highlight,
      badge: 'MINUTE MYTHS',
      icon: '⚡'
    }
  };

  const currentStyle = pipelineStyles[pipeline];

  // Intro animation for branding
  const brandingOpacity = interpolate(progress, [0, 0.05, 0.95, 1], [0, 1, 1, 0.8]);

  return (
    <div
      style={{
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        height: '120px',
        background: `linear-gradient(180deg, ${colors.background} 0%, ${colors.background}ee 70%, ${colors.background}cc 100%)`,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '0 40px',
        opacity: brandingOpacity,
        boxShadow: '0 4px 8px rgba(0, 0, 0, 0.3)',
      }}
    >
      {/* Left side - Underground Stories Logo */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
        <div
          style={{
            fontSize: '28px',
            fontWeight: 'bold',
            fontFamily: 'Arial Black, sans-serif',
            color: colors.text,
            textShadow: '2px 2px 4px rgba(0, 0, 0, 0.7)',
          }}
        >
          🕳️ UNDERGROUND STORIES
        </div>
        
        {/* Episode title */}
        <div
          style={{
            fontSize: '18px',
            fontFamily: 'Arial, sans-serif',
            color: colors.accent,
            maxWidth: '600px',
            overflow: 'hidden',
            textOverflow: 'ellipsis',
            whiteSpace: 'nowrap',
          }}
        >
          {title}
        </div>
      </div>

      {/* Right side - Episode info and pipeline badge */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
        {/* Episode number */}
        <div
          style={{
            background: currentStyle.color,
            color: colors.background,
            padding: '8px 16px',
            borderRadius: '20px',
            fontSize: '16px',
            fontWeight: 'bold',
            fontFamily: 'Arial, sans-serif',
          }}
        >
          EP.{episode}
        </div>

        {/* Pipeline badge */}
        <div
          style={{
            background: `linear-gradient(135deg, ${currentStyle.color} 0%, ${currentStyle.color}cc 100%)`,
            color: colors.text,
            padding: '10px 20px',
            borderRadius: '25px',
            fontSize: '14px',
            fontWeight: 'bold',
            fontFamily: 'Arial, sans-serif',
            textShadow: '1px 1px 2px rgba(0, 0, 0, 0.5)',
            boxShadow: '0 2px 4px rgba(0, 0, 0, 0.3)',
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
          }}
        >
          <span>{currentStyle.icon}</span>
          {currentStyle.badge}
        </div>
      </div>
    </div>
  );
};