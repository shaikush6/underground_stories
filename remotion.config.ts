import { Config } from '@remotion/cli/config';

Config.setVideoImageFormat('jpeg');
Config.setPixelFormat('yuv420p');
Config.setCodec('h264');
Config.setCrf(18); // High quality for YouTube
Config.setImageSequence(false);
Config.setOverwriteOutput(true);

// Enable concurrent rendering for better performance
Config.setConcurrency(2);

// Set scale for better performance on larger compositions
Config.setScale(1);