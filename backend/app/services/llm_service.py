import os

from openai import OpenAI

from app.config import OPENAI_API_KEY


class LLMService:
    """OpenAI-backed service with graceful local fallback."""

    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

    def generate(self, prompt: str):
        if not self.client:
            return {
                "prompt": prompt,
                "response": "I can help with job search strategy, resume targeting, interview preparation, and application tracking. Tell me what specific career task you want to work on.",
            }

        try:
            completion = self.client.responses.create(
                model="gpt-4o-mini",
                input=prompt,
            )
            text = getattr(completion, "output_text", None) or str(completion)
            return {"prompt": prompt, "response": text}
        except Exception:
            return {
                "prompt": prompt,
                "response": "I am ready to help with your career goals. Ask me about jobs, resume optimization, interviews, or LinkedIn strategy.",
            }
