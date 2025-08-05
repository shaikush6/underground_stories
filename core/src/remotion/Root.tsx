import React from 'react';
import { Composition, registerRoot } from 'remotion';
import { UndergroundVideo } from './components/UndergroundVideo';

// Define the props interface for our video composition
export interface VideoProps {
  title: string;
  episode: number;
  pipeline: 'fairer-tales' | 'timeless-retold' | 'minute-myths';
  audioPath: string;
  duration: number; // in seconds
}

const RemotionRoot: React.FC = () => {
  return (
    <>
      {/* FAIRER TALES - COMPLETE PRODUCTION SYSTEM */}
      {/* 11 Stories × 3 Parts = 33 Videos Total */}
      {/* 8-10 minutes per part, Monday/Wednesday/Friday releases */}
      
      {/* Huff & Heal - Part 1/3 */}
      <Composition
        id="huff-and-heal-part1"
        component={UndergroundVideo}
        durationInFrames={18000} // 600 seconds (10 minutes) * 30 fps
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{
          title: "Underground: Huff and Heal Part 1/3 | Fairer Tales",
          episode: 1,
          pipeline: 'fairer-tales',
          audioPath: 'Huff_&_Heal_Part1.mp3',
          duration: 600
        }}
      />
      {/* Huff & Heal - Part 2/3 */}
      <Composition
        id="huff-and-heal-part2"
        component={UndergroundVideo}
        durationInFrames={18000} // 600 seconds (10 minutes) * 30 fps
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{
          title: "Underground: Huff and Heal Part 2/3 | Fairer Tales",
          episode: 2,
          pipeline: 'fairer-tales',
          audioPath: 'Huff_&_Heal_Part2.mp3',
          duration: 600
        }}
      />
      {/* Huff & Heal - Part 3/3 */}
      <Composition
        id="huff-and-heal-part3"
        component={UndergroundVideo}
        durationInFrames={18000} // 600 seconds (10 minutes) * 30 fps
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{
          title: "Underground: Huff and Heal Part 3/3 | Fairer Tales",
          episode: 3,
          pipeline: 'fairer-tales',
          audioPath: 'Huff_&_Heal_Part3.mp3',
          duration: 600
        }}
      />
      {/* Blowback - Part 1/3 */}
      <Composition
        id="blowback-part1"
        component={UndergroundVideo}
        durationInFrames={18000} // 600 seconds (10 minutes) * 30 fps
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{
          title: "Underground: Blowback Part 1/3 | Fairer Tales",
          episode: 1,
          pipeline: 'fairer-tales',
          audioPath: 'Blowback_Part1.mp3',
          duration: 600
        }}
      />
      {/* Blowback - Part 2/3 */}
      <Composition
        id="blowback-part2"
        component={UndergroundVideo}
        durationInFrames={18000} // 600 seconds (10 minutes) * 30 fps
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{
          title: "Underground: Blowback Part 2/3 | Fairer Tales",
          episode: 2,
          pipeline: 'fairer-tales',
          audioPath: 'Blowback_Part2.mp3',
          duration: 600
        }}
      />
      {/* Blowback - Part 3/3 */}
      <Composition
        id="blowback-part3"
        component={UndergroundVideo}
        durationInFrames={18000} // 600 seconds (10 minutes) * 30 fps
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{
          title: "Underground: Blowback Part 3/3 | Fairer Tales",
          episode: 3,
          pipeline: 'fairer-tales',
          audioPath: 'Blowback_Part3.mp3',
          duration: 600
        }}
      />
      {/* Cinder-Debt - Part 1/3 */}
      <Composition
        id="cinder-debt-part1"
        component={UndergroundVideo}
        durationInFrames={18000} // 600 seconds (10 minutes) * 30 fps
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{
          title: "Underground: Cinder-Debt Part 1/3 | Fairer Tales",
          episode: 1,
          pipeline: 'fairer-tales',
          audioPath: 'Cinder-Debt_Part1.mp3',
          duration: 600
        }}
      />
      {/* Cinder-Debt - Part 2/3 */}
      <Composition
        id="cinder-debt-part2"
        component={UndergroundVideo}
        durationInFrames={18000} // 600 seconds (10 minutes) * 30 fps
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{
          title: "Underground: Cinder-Debt Part 2/3 | Fairer Tales",
          episode: 2,
          pipeline: 'fairer-tales',
          audioPath: 'Cinder-Debt_Part2.mp3',
          duration: 600
        }}
      />
      {/* Cinder-Debt - Part 3/3 */}
      <Composition
        id="cinder-debt-part3"
        component={UndergroundVideo}
        durationInFrames={18000} // 600 seconds (10 minutes) * 30 fps
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{
          title: "Underground: Cinder-Debt Part 3/3 | Fairer Tales",
          episode: 3,
          pipeline: 'fairer-tales',
          audioPath: 'Cinder-Debt_Part3.mp3',
          duration: 600
        }}
      />
      {/* Hairloom - Part 1/3 */}
      <Composition
        id="hairloom-part1"
        component={UndergroundVideo}
        durationInFrames={18000} // 600 seconds (10 minutes) * 30 fps
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{
          title: "Underground: Hairloom Part 1/3 | Fairer Tales",
          episode: 1,
          pipeline: 'fairer-tales',
          audioPath: 'Hairloom_Part1.mp3',
          duration: 600
        }}
      />
      {/* Hairloom - Part 2/3 */}
      <Composition
        id="hairloom-part2"
        component={UndergroundVideo}
        durationInFrames={18000} // 600 seconds (10 minutes) * 30 fps
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{
          title: "Underground: Hairloom Part 2/3 | Fairer Tales",
          episode: 2,
          pipeline: 'fairer-tales',
          audioPath: 'Hairloom_Part2.mp3',
          duration: 600
        }}
      />
      {/* Hairloom - Part 3/3 */}
      <Composition
        id="hairloom-part3"
        component={UndergroundVideo}
        durationInFrames={18000} // 600 seconds (10 minutes) * 30 fps
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{
          title: "Underground: Hairloom Part 3/3 | Fairer Tales",
          episode: 3,
          pipeline: 'fairer-tales',
          audioPath: 'Hairloom_Part3.mp3',
          duration: 600
        }}
      />
      {/* High Crimes - Part 1/3 */}
      <Composition
        id="high-crimes-part1"
        component={UndergroundVideo}
        durationInFrames={18000} // 600 seconds (10 minutes) * 30 fps
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{
          title: "Underground: High Crimes Part 1/3 | Fairer Tales",
          episode: 1,
          pipeline: 'fairer-tales',
          audioPath: 'High_Crimes_Part1.mp3',
          duration: 600
        }}
      />
      {/* High Crimes - Part 2/3 */}
      <Composition
        id="high-crimes-part2"
        component={UndergroundVideo}
        durationInFrames={18000} // 600 seconds (10 minutes) * 30 fps
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{
          title: "Underground: High Crimes Part 2/3 | Fairer Tales",
          episode: 2,
          pipeline: 'fairer-tales',
          audioPath: 'High_Crimes_Part2.mp3',
          duration: 600
        }}
      />
      {/* High Crimes - Part 3/3 */}
      <Composition
        id="high-crimes-part3"
        component={UndergroundVideo}
        durationInFrames={18000} // 600 seconds (10 minutes) * 30 fps
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{
          title: "Underground: High Crimes Part 3/3 | Fairer Tales",
          episode: 3,
          pipeline: 'fairer-tales',
          audioPath: 'High_Crimes_Part3.mp3',
          duration: 600
        }}
      />
      {/* Just-Right Trap - Part 1/3 */}
      <Composition
        id="just-right-trap-part1"
        component={UndergroundVideo}
        durationInFrames={18000} // 600 seconds (10 minutes) * 30 fps
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{
          title: "Underground: Just-Right Trap Part 1/3 | Fairer Tales",
          episode: 1,
          pipeline: 'fairer-tales',
          audioPath: 'Just-Right_Trap_Part1.mp3',
          duration: 600
        }}
      />
      {/* Just-Right Trap - Part 2/3 */}
      <Composition
        id="just-right-trap-part2"
        component={UndergroundVideo}
        durationInFrames={18000} // 600 seconds (10 minutes) * 30 fps
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{
          title: "Underground: Just-Right Trap Part 2/3 | Fairer Tales",
          episode: 2,
          pipeline: 'fairer-tales',
          audioPath: 'Just-Right_Trap_Part2.mp3',
          duration: 600
        }}
      />
      {/* Just-Right Trap - Part 3/3 */}
      <Composition
        id="just-right-trap-part3"
        component={UndergroundVideo}
        durationInFrames={18000} // 600 seconds (10 minutes) * 30 fps
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{
          title: "Underground: Just-Right Trap Part 3/3 | Fairer Tales",
          episode: 3,
          pipeline: 'fairer-tales',
          audioPath: 'Just-Right_Trap_Part3.mp3',
          duration: 600
        }}
      />
      {/* Mirror Error - Part 1/3 */}
      <Composition
        id="mirror-error-part1"
        component={UndergroundVideo}
        durationInFrames={18000} // 600 seconds (10 minutes) * 30 fps
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{
          title: "Underground: Mirror Error Part 1/3 | Fairer Tales",
          episode: 1,
          pipeline: 'fairer-tales',
          audioPath: 'Mirror_Error_Part1.mp3',
          duration: 600
        }}
      />
      {/* Mirror Error - Part 2/3 */}
      <Composition
        id="mirror-error-part2"
        component={UndergroundVideo}
        durationInFrames={18000} // 600 seconds (10 minutes) * 30 fps
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{
          title: "Underground: Mirror Error Part 2/3 | Fairer Tales",
          episode: 2,
          pipeline: 'fairer-tales',
          audioPath: 'Mirror_Error_Part2.mp3',
          duration: 600
        }}
      />
      {/* Mirror Error - Part 3/3 */}
      <Composition
        id="mirror-error-part3"
        component={UndergroundVideo}
        durationInFrames={18000} // 600 seconds (10 minutes) * 30 fps
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{
          title: "Underground: Mirror Error Part 3/3 | Fairer Tales",
          episode: 3,
          pipeline: 'fairer-tales',
          audioPath: 'Mirror_Error_Part3.mp3',
          duration: 600
        }}
      />
      {/* Never Grown - Part 1/3 */}
      <Composition
        id="never-grown-part1"
        component={UndergroundVideo}
        durationInFrames={18000} // 600 seconds (10 minutes) * 30 fps
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{
          title: "Underground: Never Grown Part 1/3 | Fairer Tales",
          episode: 1,
          pipeline: 'fairer-tales',
          audioPath: 'Never_Grown_Part1.mp3',
          duration: 600
        }}
      />
      {/* Never Grown - Part 2/3 */}
      <Composition
        id="never-grown-part2"
        component={UndergroundVideo}
        durationInFrames={18000} // 600 seconds (10 minutes) * 30 fps
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{
          title: "Underground: Never Grown Part 2/3 | Fairer Tales",
          episode: 2,
          pipeline: 'fairer-tales',
          audioPath: 'Never_Grown_Part2.mp3',
          duration: 600
        }}
      />
      {/* Never Grown - Part 3/3 */}
      <Composition
        id="never-grown-part3"
        component={UndergroundVideo}
        durationInFrames={18000} // 600 seconds (10 minutes) * 30 fps
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{
          title: "Underground: Never Grown Part 3/3 | Fairer Tales",
          episode: 3,
          pipeline: 'fairer-tales',
          audioPath: 'Never_Grown_Part3.mp3',
          duration: 600
        }}
      />
      {/* Spin Cycle - Part 1/3 */}
      <Composition
        id="spin-cycle-part1"
        component={UndergroundVideo}
        durationInFrames={18000} // 600 seconds (10 minutes) * 30 fps
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{
          title: "Underground: Spin Cycle Part 1/3 | Fairer Tales",
          episode: 1,
          pipeline: 'fairer-tales',
          audioPath: 'Spin_Cycle_Part1.mp3',
          duration: 600
        }}
      />
      {/* Spin Cycle - Part 2/3 */}
      <Composition
        id="spin-cycle-part2"
        component={UndergroundVideo}
        durationInFrames={18000} // 600 seconds (10 minutes) * 30 fps
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{
          title: "Underground: Spin Cycle Part 2/3 | Fairer Tales",
          episode: 2,
          pipeline: 'fairer-tales',
          audioPath: 'Spin_Cycle_Part2.mp3',
          duration: 600
        }}
      />
      {/* Spin Cycle - Part 3/3 */}
      <Composition
        id="spin-cycle-part3"
        component={UndergroundVideo}
        durationInFrames={18000} // 600 seconds (10 minutes) * 30 fps
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{
          title: "Underground: Spin Cycle Part 3/3 | Fairer Tales",
          episode: 3,
          pipeline: 'fairer-tales',
          audioPath: 'Spin_Cycle_Part3.mp3',
          duration: 600
        }}
      />
      {/* Stockholm - Part 1/3 */}
      <Composition
        id="stockholm-part1"
        component={UndergroundVideo}
        durationInFrames={18000} // 600 seconds (10 minutes) * 30 fps
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{
          title: "Underground: Stockholm Part 1/3 | Fairer Tales",
          episode: 1,
          pipeline: 'fairer-tales',
          audioPath: 'Stockholm_Part1.mp3',
          duration: 600
        }}
      />
      {/* Stockholm - Part 2/3 */}
      <Composition
        id="stockholm-part2"
        component={UndergroundVideo}
        durationInFrames={18000} // 600 seconds (10 minutes) * 30 fps
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{
          title: "Underground: Stockholm Part 2/3 | Fairer Tales",
          episode: 2,
          pipeline: 'fairer-tales',
          audioPath: 'Stockholm_Part2.mp3',
          duration: 600
        }}
      />
      {/* Stockholm - Part 3/3 */}
      <Composition
        id="stockholm-part3"
        component={UndergroundVideo}
        durationInFrames={18000} // 600 seconds (10 minutes) * 30 fps
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{
          title: "Underground: Stockholm Part 3/3 | Fairer Tales",
          episode: 3,
          pipeline: 'fairer-tales',
          audioPath: 'Stockholm_Part3.mp3',
          duration: 600
        }}
      />
      {/* Sugar Shelter - Part 1/3 */}
      <Composition
        id="sugar-shelter-part1"
        component={UndergroundVideo}
        durationInFrames={18000} // 600 seconds (10 minutes) * 30 fps
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{
          title: "Underground: Sugar Shelter Part 1/3 | Fairer Tales",
          episode: 1,
          pipeline: 'fairer-tales',
          audioPath: 'Sugar_Shelter_Part1.mp3',
          duration: 600
        }}
      />
      {/* Sugar Shelter - Part 2/3 */}
      <Composition
        id="sugar-shelter-part2"
        component={UndergroundVideo}
        durationInFrames={18000} // 600 seconds (10 minutes) * 30 fps
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{
          title: "Underground: Sugar Shelter Part 2/3 | Fairer Tales",
          episode: 2,
          pipeline: 'fairer-tales',
          audioPath: 'Sugar_Shelter_Part2.mp3',
          duration: 600
        }}
      />
      {/* Sugar Shelter - Part 3/3 */}
      <Composition
        id="sugar-shelter-part3"
        component={UndergroundVideo}
        durationInFrames={18000} // 600 seconds (10 minutes) * 30 fps
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{
          title: "Underground: Sugar Shelter Part 3/3 | Fairer Tales",
          episode: 3,
          pipeline: 'fairer-tales',
          audioPath: 'Sugar_Shelter_Part3.mp3',
          duration: 600
        }}
      />
      
      {/* Test Compositions */}
      <Composition
        id="huff-heal-3min-sample"
        component={UndergroundVideo}
        durationInFrames={5400} // 180 seconds * 30 fps
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{
          title: "Underground: Huff & Heal Part 1/3 Sample | Fairer Tales",
          episode: 1,
          pipeline: 'fairer-tales',
          audioPath: 'Huff_and_Heal_Complete_Episode.mp3',
          duration: 180
        }}
      />
    </>
  );
};

registerRoot(RemotionRoot);
