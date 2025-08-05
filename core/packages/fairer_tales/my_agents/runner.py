import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Agent:
    def __init__(self, name: str, instructions: str):
        self.name = name
        self.instructions = instructions

class Runner:
    @staticmethod
    def run_sync(agent: Agent, input_text: str):
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": agent.instructions},
                {"role": "user", "content": input_text}
            ],
            temperature=0.4
        )
        return response.choices[0].message.content