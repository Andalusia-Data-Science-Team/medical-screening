import os
from openai import OpenAI
from typing import List, Optional
from langchain.llms.base import LLM
from helpers import Inquiry
from dotenv import load_dotenv

class FireworksLLM(LLM):
    model: str
    api_key: str
    base_url: str = "https://api.fireworks.ai/inference/v1"
    temperature: float = 0
    top_p: float = 0

    @property
    def _llm_type(self) -> str:
        return "fireworks"

    def _call(
        self,
        user_prompt: str,
        system_prompt: Optional[str] = None,
    ) -> str:
        """
        Calls the Fireworks chat completion API.

        Args:
            user_prompt (str): The user input (e.g., formatted from USER_PROMPT_TEMPLATE).
            stop (list, optional): Stop tokens (not used here but available).
            system_prompt (str, optional): System-level instruction.

        Returns:
            str: Model response content
        """
        client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
        )

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": user_prompt})

        response = client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            top_p=self.top_p,
        )

        return response.choices[0].message.content


# Load environment variables
load_dotenv()
api_key = os.getenv("FIREWORKS_API_KEY")
model_name = os.getenv("MODEL_NAME")

# Instantiate default LLM
fireworks_llm = FireworksLLM(
    model=model_name,
    api_key=api_key,
)