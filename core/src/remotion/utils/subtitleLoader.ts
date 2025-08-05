// Subtitle Data Loader for Remotion Components
// Loads Whisper-generated subtitle JSON files

export interface SubtitleSegment {
  text: string;
  start: number;
  end: number;
}

export interface SubtitleData {
  audio_file: string;
  total_segments: number;
  segments: SubtitleSegment[];
  generated_at: string;
  format: string;
}

// Cache for loaded subtitle data
const subtitleCache: Map<string, SubtitleData | null> = new Map();

export const loadSubtitleData = async (audioFilename: string): Promise<SubtitleData | null> => {
  // Check cache first
  if (subtitleCache.has(audioFilename)) {
    return subtitleCache.get(audioFilename) || null;
  }

  try {
    const subtitleFilename = audioFilename.replace('.mp3', '_subtitles.json');
    
    // In production, this would load from the subtitles directory
    // For now, we'll use a dynamic import approach
    const response = await fetch(`/subtitles/${subtitleFilename}`);
    
    if (!response.ok) {
      console.log(`Subtitle file not found: ${subtitleFilename}`);
      subtitleCache.set(audioFilename, null);
      return null;
    }
    
    const subtitleData: SubtitleData = await response.json();
    subtitleCache.set(audioFilename, subtitleData);
    
    console.log(`Loaded ${subtitleData.total_segments} subtitle segments for ${audioFilename}`);
    return subtitleData;
    
  } catch (error) {
    console.error(`Error loading subtitle data for ${audioFilename}:`, error);
    subtitleCache.set(audioFilename, null);
    return null;
  }
};

export const getSubtitleSegmentAtTime = (
  subtitleData: SubtitleData | null, 
  currentTime: number
): SubtitleSegment | null => {
  if (!subtitleData || !subtitleData.segments) {
    return null;
  }
  
  return subtitleData.segments.find(segment => 
    currentTime >= segment.start && currentTime < segment.end
  ) || null;
};
