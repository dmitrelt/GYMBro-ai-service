# app/llm.py

import json
from openai import AsyncOpenAI
from pydantic import BaseModel
from typing import Type
from app.config import settings


class LLMClient:

    def __init__(self):
        """Инициализация клиента Groq"""
        self.client = AsyncOpenAI(
            api_key=settings.GROQ_API_KEY,
            base_url="https://api.groq.com/openai/v1"
        )
        self.model = settings.GROQ_MODEL

    async def generate_structured(
        self,
        prompt: str,
        response_model: Type[BaseModel],
        temperature: float = 0.3
    ) -> BaseModel:

        try:
            completion = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Ты точный парсер и фитнес-ассистент. "
                            "Всегда отвечай строго в JSON по указанной схеме. "
                            "Не добавляй никакого дополнительного текста, объяснений или markdown."
                        )
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                response_format={"type": "json_object"}
            )

            raw_text = completion.choices[0].message.content
            parsed_dict = json.loads(raw_text)

            return response_model(**parsed_dict)

        except json.JSONDecodeError:
            raise ValueError("Groq вернул некорректный JSON. Проверь промпт.")
        except Exception as e:
            raise Exception(f"Ошибка при обращении к Groq API: {str(e)}")


llm_client = LLMClient()