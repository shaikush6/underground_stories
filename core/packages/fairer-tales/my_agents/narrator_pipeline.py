# === narrator_pipeline.py ===

import os
import json
import asyncio
from pathlib import Path
from pydub import AudioSegment
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

from character_config import CHARACTER_STYLE_PROMPTS, SPEAKER_ALIAS_MAP

async def synthesize_narrator_voice(script_path: str, output_path: str):
    print(f"📖 Loading script from: {script_path}")
    with open(script_path, "r", encoding="utf-8") as f:
        script_data = json.load(f)

    output_path = Path(output_path)
    chunk_dir = output_path / "narrator_chunks"
    final_path = output_path / "chapter_narrator.wav"

    chunk_dir.mkdir(parents=True, exist_ok=True)
    combined = AudioSegment.empty()

    for i, line in enumerate(script_data):
        raw_speaker = line.get("speaker", "Narrator")
        speaker = SPEAKER_ALIAS_MAP.get(raw_speaker, raw_speaker)
        voice = "ash"  # fixed single narrator
        text = line.get("text", "")

        instructions = CHARACTER_STYLE_PROMPTS.get(speaker, "")

        chunk_path = chunk_dir / f"line_{i + 1:03d}.wav"
        print(f"🎤 [{speaker}] | Line {i + 1}/{len(script_data)}")

        async with client.audio.speech.with_streaming_response.create(
                model="gpt-4o-mini-tts",
                voice=voice,
                input=text,
                instructions=instructions,
                response_format="wav"
        ) as response:
            with open(chunk_path, "wb") as f:
                async for part in response.iter_bytes():
                    f.write(part)

        audio = AudioSegment.from_wav(chunk_path)
        combined += audio + AudioSegment.silent(duration=300)

    combined.export(final_path, format="wav")
    print(f"✅ Final narrator chapter saved to: {final_path.resolve()}")
