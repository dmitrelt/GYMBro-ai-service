import json
from typing import Type
from openai import AsyncOpenAI
from pydantic import BaseModel

from app.config import settings

class LLMClient:
    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=settings.GROQ_API_KEY,
            base_url="https://api.groq.com/openai/v1"
        )
        self.model = settings.GROQ_MODEL

    async def generate_structured(
        self,
        system_prompt: str,
        user_prompt: str,
        response_model: Type[BaseModel],
        temperature: float = 0.3
    ) -> BaseModel:
        try:
            completion = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature,
                response_format={"type": "json_object"}
            )

            raw_text = completion.choices[0].message.content.strip()
            parsed_dict = json.loads(raw_text)
            return response_model(**parsed_dict)

        except json.JSONDecodeError as e:
            raise ValueError(f"LLM вернул некорректный JSON: {raw_text[:300]}...") from e
        except Exception as e:
            raise Exception(f"Ошибка Groq API: {e}") from e


llm_client = LLMClient()