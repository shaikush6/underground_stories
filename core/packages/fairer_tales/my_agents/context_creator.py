# my_agents/context_agent.py

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def run_context_agent(narration_units: list, model="o4-mini") -> list:
    """
    For each narration unit, analyze the emotional and situational context,
    and generate a detailed directive for voice performance.

    Each result should include expanded delivery notes for the speaker
    that account for:
    - Scene tension or calm
    - Interpersonal conflict or harmony
    - Urgency, fear, sarcasm, pride, curiosity, etc.
    - Internal states vs. external dialogue

    Output format:
    [
        {
            "speaker": "Lord Roxton",
            "text": "This place gives me the creeps...",
            "context_directive": "Voice: Low and cautious. Delivery: quick but quiet. Tone: uneasy but alert. Emotion: wary."
        },
        ...
    ]
    """
    prompt = (
        "You are a voice acting director."
        " For each narration line from an audiobook script, analyze the situation and speaker's mindset."
        " Your task is to generate a full context-aware delivery directive."
        " Include the speaker's emotional state, urgency, and social subtext."
        " Think like a theater director or film coach guiding an actor for a performance."
        " The goal is to give each character an emotionally accurate, engaging read."
        " Do NOT summarize the line. Instead, provide a styled delivery plan."
        " Format each as JSON object with 'speaker', 'text', and 'context_directive'."
        " Return only the list of directives."
    )

    input_data = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": f"Here is the narration list:\n{narration_units}"}
    ]

    response = client.responses.create(
        model=model,
        input=input_data,
        text={"format": {"type": "text"}},
        reasoning={"effort": "high"},
        tools=[]
    )

    return response.output

