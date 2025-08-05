import React from 'react';
import { interpolate, Easing } from 'remotion';

interface ProgressiveSketchProps {
  progress: number; // 0 to 1
  pipeline: 'fairer-tales' | 'timeless-retold' | 'minute-myths';
  episode: number;
  storyType?: string;
}

export const ProgressiveSketch: React.FC<ProgressiveSketchProps> = ({
  progress,
  pipeline,
  storyType = 'default'
}) => {
  
  // Define drawing stages for "Huff & Heal" wolf therapist story
  const wolfTherapistStages = [
    { start: 0.0, end: 0.15, element: 'wolf-outline' },        // Simple wolf silhouette
    { start: 0.15, end: 0.3, element: 'forest-circle' },       // Therapy circle in forest
    { start: 0.3, end: 0.5, element: 'woodland-animals' },     // Animals approaching
    { start: 0.5, end: 0.7, element: 'therapy-session' },      // Interaction details
    { start: 0.7, end: 0.85, element: 'healing-sanctuary' },   // Sanctuary environment
    { start: 0.85, end: 1.0, element: 'resolution' },          // Final peaceful scene
  ];

  // Calculate individual element progress
  const getElementProgress = (start: number, end: number) => {
    return interpolate(progress, [start, end], [0, 1], {
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
      easing: Easing.out(Easing.cubic)
    });
  };

  // Underground Stories color palette
  const colors = {
    primary: '#B87333',      // Copper
    secondary: '#00BFFF',    // Electric blue  
    accent: '#F5F5F5',       // Off-white
    forest: '#2d5016',       // Forest green
    earth: '#4a3728',        // Earth brown
  };

  // SVG drawing functions for each story element
  const WolfOutline = ({ progress: elemProgress }: { progress: number }) => {
    const pathLength = 1000; // Approximate path length
    const dashOffset = pathLength * (1 - elemProgress);
    
    return (
      <g transform="translate(960, 400)"> {/* Center of main area */}
        <path
          d="M-80,-60 C-60,-80 -40,-85 -20,-80 C0,-85 20,-85 40,-80 C60,-85 80,-60 80,-40 
             C85,-20 80,0 75,20 C70,40 60,55 40,60 L40,80 C35,90 25,95 15,90 
             C5,95 -5,95 -15,90 C-25,95 -35,90 -40,80 L-40,60 
             C-60,55 -70,40 -75,20 C-80,0 -85,-20 -80,-40 Z
             M-60,-30 C-58,-35 -55,-35 -52,-30 C-50,-25 -52,-20 -55,-20 C-58,-20 -60,-25 -60,-30 Z
             M52,-30 C55,-35 58,-35 60,-30 C60,-25 58,-20 55,-20 C52,-20 50,-25 52,-30 Z
             M-15,0 L0,-5 L15,0 L10,10 L5,15 L0,12 L-5,15 L-10,10 Z"
          fill="none"
          stroke={colors.primary}
          strokeWidth="3"
          strokeDasharray={pathLength}
          strokeDashoffset={dashOffset}
          style={{
            transition: 'stroke-dashoffset 0.5s ease-out'
          }}
        />
        
        {/* Wolf ears - appear after main outline */}
        {elemProgress > 0.5 && (
          <>
            <path
              d="M-40,-65 L-50,-85 L-30,-80 Z M30,-80 L50,-85 L40,-65 Z"
              fill="none"
              stroke={colors.primary}
              strokeWidth="2"
              opacity={interpolate(elemProgress, [0.5, 0.8], [0, 1])}
            />
          </>
        )}
      </g>
    );
  };

  const ForestCircle = ({ progress: elemProgress }: { progress: number }) => {
    const numTrees = 8;
    const radius = 200;
    
    return (
      <g transform="translate(960, 370)">
        {/* Therapy circle boundary */}
        <circle
          cx={0}
          cy={0}
          r={radius}
          fill="none"
          stroke={colors.forest}
          strokeWidth="2"
          strokeDasharray="10,5"
          opacity={interpolate(elemProgress, [0, 0.3], [0, 0.6])}
        />
        
        {/* Trees around the circle */}
        {Array.from({ length: numTrees }).map((_, i) => {
          const angle = (i / numTrees) * 2 * Math.PI;
          const x = Math.cos(angle) * radius;
          const y = Math.sin(angle) * radius;
          const treeProgress = interpolate(elemProgress, [0.2, 0.8], [0, 1]);
          const individualDelay = i * 0.1;
          const delayedProgress = interpolate(treeProgress, [individualDelay, individualDelay + 0.3], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp'
          });
          
          if (delayedProgress <= 0) return null;
          
          return (
            <g key={i} transform={`translate(${x}, ${y})`}>
              {/* Tree trunk */}
              <rect
                x={-5}
                y={0}
                width={10}
                height={30 * delayedProgress}
                fill={colors.earth}
              />
              {/* Tree foliage */}
              <circle
                cx={0}
                cy={-10}
                r={15 * delayedProgress}
                fill={colors.forest}
                opacity={0.8}
              />
            </g>
          );
        })}
      </g>
    );
  };

  const WoodlandAnimals = ({ progress: elemProgress }: { progress: number }) => {
    const animals = [
      { x: 800, y: 450, type: 'rabbit', delay: 0 },
      { x: 1120, y: 420, type: 'squirrel', delay: 0.2 },
      { x: 850, y: 380, type: 'bird', delay: 0.4 },
      { x: 1070, y: 480, type: 'fox', delay: 0.6 },
    ];

    return (
      <g>
        {animals.map((animal, i) => {
          const animalProgress = interpolate(elemProgress, [animal.delay, animal.delay + 0.4], [0, 1], {
            extrapolateLeft: 'clamp',
            extrapolateRight: 'clamp'
          });
          
          if (animalProgress <= 0) return null;
          
          return (
            <g key={i} transform={`translate(${animal.x}, ${animal.y})`}>
              {/* Simple animal silhouettes */}
              {animal.type === 'rabbit' && (
                <g opacity={animalProgress}>
                  <ellipse cx={0} cy={5} rx={12} ry={8} fill={colors.accent} />
                  <circle cx={0} cy={-5} r={6} fill={colors.accent} />
                  <ellipse cx={-3} cy={-12} rx={2} ry={6} fill={colors.accent} />
                  <ellipse cx={3} cy={-12} rx={2} ry={6} fill={colors.accent} />
                </g>
              )}
              
              {animal.type === 'squirrel' && (
                <g opacity={animalProgress}>
                  <ellipse cx={0} cy={0} rx={8} ry={12} fill={colors.accent} />
                  <circle cx={0} cy={-8} r={5} fill={colors.accent} />
                  <path d="M-8,-5 Q-15,-15 -20,-5 Q-15,5 -8,0" fill={colors.accent} />
                </g>
              )}
              
              {animal.type === 'bird' && (
                <g opacity={animalProgress}>
                  <ellipse cx={0} cy={0} rx={6} ry={4} fill={colors.secondary} />
                  <path d="M-8,-2 L-15,-5 L-12,0 L-15,5 L-8,2" fill={colors.secondary} />
                  <path d="M8,-2 L15,-5 L12,0 L15,5 L8,2" fill={colors.secondary} />
                </g>
              )}
              
              {animal.type === 'fox' && (
                <g opacity={animalProgress}>
                  <ellipse cx={0} cy={3} rx={15} ry={6} fill="#cc6600" />
                  <circle cx={8} cy={-2} r={4} fill="#cc6600" />
                  <path d="M6,-6 L10,-10 L14,-6" fill="#cc6600" />
                  <path d="M2,-6 L6,-10 L10,-6" fill="#cc6600" />
                </g>
              )}
            </g>
          );
        })}
      </g>
    );
  };

  const TherapySession = ({ progress: elemProgress }: { progress: number }) => {
    return (
      <g transform="translate(960, 370)">
        {/* Gentle interaction indicators */}
        <g opacity={interpolate(elemProgress, [0, 0.5], [0, 0.8])}>
          {/* Healing energy/connection lines */}
          <path
            d="M-60,20 Q-30,0 0,20 Q30,0 60,20"
            stroke={colors.secondary}
            strokeWidth="2"
            fill="none"
            opacity={0.6}
            strokeDasharray="5,5"
          />
          <path
            d="M-40,40 Q0,20 40,40"
            stroke={colors.secondary}
            strokeWidth="1"
            fill="none"
            opacity={0.4}
            strokeDasharray="3,3"
          />
        </g>
        
        {/* Peaceful symbols */}
        {elemProgress > 0.6 && (
          <g opacity={interpolate(elemProgress, [0.6, 1], [0, 1])}>
            {/* Small hearts or peace symbols */}
            <g transform="translate(-30, -20)">
              <path
                d="M0,5 C-3,0 -8,0 -8,5 C-8,8 0,15 0,15 C0,15 8,8 8,5 C8,0 3,0 0,5 Z"
                fill={colors.primary}
                opacity={0.7}
              />
            </g>
            <g transform="translate(25, -15)">
              <path
                d="M0,5 C-3,0 -8,0 -8,5 C-8,8 0,15 0,15 C0,15 8,8 8,5 C8,0 3,0 0,5 Z"
                fill={colors.secondary}
                opacity={0.7}
              />
            </g>
          </g>
        )}
      </g>
    );
  };

  const HealingSanctuary = ({ progress: elemProgress }: { progress: number }) => {
    return (
      <g>
        {/* Background sanctuary elements */}
        <g opacity={interpolate(elemProgress, [0, 0.8], [0, 0.5])}>
          {/* Gentle background patterns */}
          <defs>
            <pattern id="sanctuary-pattern" x="0" y="0" width="40" height="40" patternUnits="userSpaceOnUse">
              <circle cx="20" cy="20" r="2" fill={colors.forest} opacity="0.2" />
            </pattern>
          </defs>
          <rect x="0" y="0" width="1920" height="740" fill="url(#sanctuary-pattern)" />
        </g>
        
        {/* Mystical elements */}
        {elemProgress > 0.4 && (
          <g opacity={interpolate(elemProgress, [0.4, 1], [0, 0.7])}>
            {/* Floating particles/fireflies */}
            {Array.from({ length: 12 }).map((_, i) => (
              <circle
                key={i}
                cx={200 + (i * 140) % 1520}
                cy={150 + (i * 60) % 440}
                r="3"
                fill={colors.secondary}
                opacity={Math.sin(i + elemProgress * 4) * 0.3 + 0.4}
                style={{
                  animation: `float ${3 + i * 0.5}s ease-in-out infinite`
                }}
              />
            ))}
          </g>
        )}
      </g>
    );
  };

  const Resolution = ({ progress: elemProgress }: { progress: number }) => {
    return (
      <g opacity={interpolate(elemProgress, [0, 1], [0, 1])}>
        {/* Final peaceful glow around the scene */}
        <defs>
          <radialGradient id="peaceful-glow" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stopColor={colors.secondary} stopOpacity="0.2" />
            <stop offset="70%" stopColor={colors.primary} stopOpacity="0.1" />
            <stop offset="100%" stopColor="transparent" stopOpacity="0" />
          </radialGradient>
        </defs>
        <ellipse
          cx="960"
          cy="370"
          rx="400"
          ry="300"
          fill="url(#peaceful-glow)"
        />
        
        {/* Final completion indicator */}
        {elemProgress > 0.8 && (
          <g transform="translate(960, 200)">
            <text
              textAnchor="middle"
              fill={colors.accent}
              fontSize="24"
              fontFamily="Arial, sans-serif"
              opacity={interpolate(elemProgress, [0.8, 1], [0, 0.8])}
            >
              ✨ Healing Complete ✨
            </text>
          </g>
        )}
      </g>
    );
  };

  return (
    <svg
      width="100%"
      height="100%"
      viewBox="0 0 1920 740"
      style={{ overflow: 'visible' }}
    >
      <style>
        {`
          @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
          }
        `}
      </style>
      
      {/* Render each stage based on progress */}
      {wolfTherapistStages.map((stage, index) => {
        const elemProgress = getElementProgress(stage.start, stage.end);
        
        switch (stage.element) {
          case 'wolf-outline':
            return <WolfOutline key={index} progress={elemProgress} />;
          case 'forest-circle':
            return <ForestCircle key={index} progress={elemProgress} />;
          case 'woodland-animals':
            return <WoodlandAnimals key={index} progress={elemProgress} />;
          case 'therapy-session':
            return <TherapySession key={index} progress={elemProgress} />;
          case 'healing-sanctuary':
            return <HealingSanctuary key={index} progress={elemProgress} />;
          case 'resolution':
            return <Resolution key={index} progress={elemProgress} />;
          default:
            return null;
        }
      })}
    </svg>
  );
};