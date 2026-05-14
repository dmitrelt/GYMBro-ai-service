from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from app.llm import llm_client
from app.schemas import RecommendationRequest, RecommendationResponse
from app.security import get_current_user

router = APIRouter(prefix='/recommendation', tags=['recommendation'])


@router.post('/', response_model=RecommendationResponse)
async def generate_recommendation(
    request: RecommendationRequest,
    user_id: int = Depends(get_current_user)
):
    """
    Генерация персонализированной рекомендации на основе полной статистики.
    """
    system_prompt = """
Ты профессиональный персональный тренер и нутрициолог с большим опытом.
Анализируй предоставленную структурированную статистику и давай конкретные, полезные и мотивирующие рекомендации на русском языке.

Структура ответа:
1. Краткий анализ текущего прогресса
2. Рекомендации по тренировкам на ближайшие 7-14 дней
3. Рекомендации по питанию (целевое КБЖУ и продукты)
4. Советы по восстановлению и прогрессу
5. Мотивационное заключение
"""

    user_prompt = f"""
=== ЦЕЛИ И ОГРАНИЧЕНИЯ ===
Цели: {request.goals_text}
Ограничения: {request.restrictions_text or "Не указаны"}

=== СТАТИСТИКА ТРЕНИРОВОК ===
{request.workouts.model_dump_json(indent=2)}

=== СТАТИСТИКА ПИТАНИЯ ===
{request.nutrition.model_dump_json(indent=2)}

Сегодня: {datetime.now().strftime("%Y-%m-%d")}
"""

    try:
        result = await llm_client.generate_structured(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_model=RecommendationResponse,
            temperature=0.65
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))