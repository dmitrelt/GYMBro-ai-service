from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from app.llm import llm_client
from app.schemas import TrainingParseRequest, TrainingParseResponse
from app.security import get_current_user

router = APIRouter(prefix='/training', tags=['training'])


@router.post('/parse', response_model=TrainingParseResponse)
async def parse_training(
    request: TrainingParseRequest,
    user_id: int = Depends(get_current_user)
):
    """
    Парсинг свободного текста тренировки в структурированный формат.
    """
    system_prompt = """
Ты профессиональный фитнес-тренер и очень точный парсер тренировок.
Пользователь пишет одним сообщением всё, что сделал на тренировке.

Твоя задача — разобрать текст и вернуть структурированный результат.

Правила:
- Каждое упражнение выдели отдельно.
- Название упражнения оставляй близко к тому, как написал пользователь, или используй стандартное название.
- Определи основную группу мышц (на русском: грудь, спина, ноги, плечи, бицепс, трицепс, пресс и т.д.).
- Тип упражнения укажи на русском: силовое, гипертрофия, кардио, функциональное, растяжка и т.д.
- Для каждого подхода укажи вес, повторения, длительность или дистанцию, если они есть.
- Ощущение от подхода: легко, средне, тяжело. Если не указано — ставь "средне".

Будь максимально точным и логичным. Не придумывай информацию, которой нет.
Отвечай только JSON по переданной схеме, без каких-либо дополнительных слов.
"""

    user_prompt = f"""
Тренировка пользователя за сегодня:

"{request.raw_text}"
"""

    try:
        return await llm_client.generate_structured(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_model=TrainingParseResponse,
            temperature=0.2
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))