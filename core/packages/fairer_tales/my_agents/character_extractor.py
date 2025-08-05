import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_characters_llm(chapter_text: str, model="gpt-4o-mini") -> list:
    system_prompt = (
        "You are helping build an audiobook narration system.\n"
        "Your job is to extract and analyze characters from a chapter of fiction. The chapter includes narration and dialogue.\n\n"
        "For each character you detect, return:\n"
        "- Their canonical name (the version that should be used throughout the script)\n"
        "- Any aliases or alternative names used to refer to the same person (e.g., \"Professor Challenger\" and \"Challenger\")\n"
        "- Their likely gender (male, female, unknown)\n"
        "- Whether they are major or minor in this chapter\n"
        "- Whether they appear to be recurring characters across the story\n\n"
        "### Output Format:\n"
        "Return a JSON array of characters like this:\n"
        "[\n"
        "  {\n"
        "    \"name\": \"Professor Challenger\",\n"
        "    \"aliases\": [\"Challenger\", \"the Professor\"],\n"
        "    \"gender\": \"male\",\n"
        "    \"importance\": \"major\",\n"
        "    \"recurring\": true\n"
        "  },\n"
        "  ...\n"
        "]\n\n"
        "ONLY include people (not places or abstract references).\n"
        "Use the narrator’s context to help identify people even if their names are incomplete.\n"
        "Return only the JSON, without explanations or markdown."
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": chapter_text}
        ],
        temperature=0.2
    )

    try:
        characters = json.loads(response.choices[0].message.content)
    except json.JSONDecodeError:
        print("⚠️ Failed to parse character JSON output.")
        print(response.choices[0].message.content)
        return []

    return characters