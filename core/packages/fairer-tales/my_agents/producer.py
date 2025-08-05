import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

from character_config import CHARACTER_VOICE_MAP, CHARACTER_STYLE_PROMPTS, SPEAKER_ALIAS_MAP
from my_agents.character_extractor import extract_characters_llm  # ← USE THE NEW LLM-BASED EXTRACTOR

def generate_alias_map(character_list: list) -> dict:
    alias_map = {}
    for character in character_list:
        canonical = character["name"]
        for alias in character.get("aliases", []):
            alias_map[alias] = canonical
    return alias_map

def run_producer_agent(chapter_text: str, chapter_num: int, output_dir: str = "output/text") -> str:
    """
    Given a modernized chapter text, generate a multi-voice narration script
    and save it as a JSON file.
    """

    # === STEP 1: Extract characters using the LLM extractor ===
    character_list = extract_characters_llm(chapter_text)
    print("🧾 Detected Characters:", character_list)

    alias_map = generate_alias_map(character_list)
    print("🔗 Alias Map:", alias_map)

    # === STEP 2: Dynamically assign voices ===
    AUTO_VOICE_POOL = ["ash"]  # Just use one narrator voice for all
    dynamic_voice_map = {
        character["name"]: "ash"
        for character in character_list
    }
    dynamic_voice_map["Narrator"] = "ash"
    dynamic_voice_map["Ned"] = "ash"
    dynamic_voice_map["Malone"] = "ash"

    voice_map = dynamic_voice_map

    save_character_config(voice_map, alias_map, character_list)

    # === STEP 3: Build system instructions ===
    system_instructions = (
        "You are a senior audiobook production agent tasked with turning a modernized chapter of a novel into a clean, structured narration script.\n\n"
        "Your goal is to parse the chapter into small, manageable narration units (1–3 sentences each) that will later be spoken aloud.\n\n"
        "Each narration unit must be a JSON object with:\n"
        "  - 'speaker': the name of the character or narrator\n"
        "  - 'voice': always use 'ash'\n"
        "  - 'text': the actual line to be spoken aloud\n\n"
        "Narration and scene descriptions must always be assigned to the speaker 'Narrator'.\n"
        "This story is told in first person by 'Ned Malone', so both 'Narrator', 'Malone', and 'Ned' are the same voice (Ash).\n\n"
        "If a line contains character dialogue followed by a narrator-style attribution (e.g. \"he said with a sigh\"), SPLIT it into two JSON entries:\n"
        "  • One for the character's spoken dialogue\n"
        "  • One for the narrator's attribution (use speaker='Narrator')\n\n"
        "Return ONLY the JSON array — no commentary, no markdown, no explanations.\n"
        "Strictly follow this format for consistency."
        "If you are unsure, still return a valid JSON array with at least one line formatted correctly, rather than leaving the output empty."
    )

    response = client.chat.completions.create(
        model="o4-mini",
        messages=[
            {"role": "system", "content": system_instructions},
            {"role": "user", "content": chapter_text}
        ]
    )

    script_output = response.choices[0].message.content

    if not script_output or not script_output.strip().startswith("["):
        raise ValueError("❌ Script output was empty or invalid. No JSON array found.")

    output_path = os.path.join(output_dir, f"chapter_{chapter_num}_script.json")
    os.makedirs(output_dir, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(script_output)

    print(f"✅ Script saved to: {output_path}")
    return output_path

def save_character_config(voice_map: dict, alias_map: dict, character_list: list, filepath="character_config.py"):
    def format_dict(name, data):
        return f"{name} = " + json.dumps(data, indent=2) + "\n\n"

    style_prompts = {
        c["name"]: f"""Voice: (style TBD)
Punctuation: (style TBD)
Delivery: (style TBD)
Phrasing: (style TBD)
Tone: (style TBD)
""" for c in character_list
    }

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("# Auto-generated character config\n\n")
        f.write(format_dict("CHARACTER_VOICE_MAP", voice_map))
        f.write(format_dict("CHARACTER_STYLE_PROMPTS", style_prompts))
        f.write(format_dict("SPEAKER_ALIAS_MAP", alias_map))

    print(f"🧾 character_config.py updated with {len(voice_map)} voices, {len(alias_map)} aliases, {len(style_prompts)} styles.")
