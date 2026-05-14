from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from app.llm import llm_client
from app.schemas import NutritionRequest, NutritionResponse
from app.security import get_current_user

router = APIRouter(prefix='/nutrition', tags=['nutrition'])


@router.post('/calculate', response_model=NutritionResponse)
async def calculate_nutrition(
    request: NutritionRequest,
    user_id: int = Depends(get_current_user)
):
    """
    Расчёт КБЖУ по свободному тексту питания.
    """
    system_prompt = """
Ты опытный нутрициолог и эксперт по составу продуктов питания.

Пользователь пишет в свободной форме, что он съел за приём пищи или за день.
Твоя задача — рассчитать КБЖУ максимально точно и реалистично.

Правила:
- Если пользователь указал граммовку — используй её.
- Если граммовка не указана — выбери разумный размер одной стандартной порции этого блюда.
- Для сложных блюд можешь разбить на основные компоненты.
- Используй реальные средние значения КБЖУ для продуктов.
- Будь точным, но не занижай и не завышай сильно.

Отвечай строго JSON по схеме, без каких-либо дополнительных комментариев и объяснений.
"""

    user_prompt = f"""
Что съел пользователь:

"{request.raw_text}"
"""

    try:
        return await llm_client.generate_structured(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_model=NutritionResponse,
            temperature=0.2
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))