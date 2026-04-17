import json
import httpx
from pydantic import BaseModel
from typing import Type, Any
from app.config import settings


class LLMClient:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.model = settings.GEMINI_MODEL

    async def generate_structured(
            self,
            prompt: str,
            response_model: Type[BaseModel],
            temperature: float = 0.3
    ) -> Any:

        url = (f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:"
               f"generateContent?key={self.api_key}")

        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ],
            "generationConfig": {
                "temperature": temperature,
                "responseMimeType": "application/json"
            }
        }

        async with httpx.AsyncClient(timeout=40.0) as client:
            response = await client.post(url, json=payload)

            response.raise_for_status()

            data = response.json()

            raw_text = data['candidates'][0]['content']['parts'][0]['text']

            parsed_dict = json.loads(raw_text)

            return response_model(**parsed_dict)


llm_client = LLMClient()