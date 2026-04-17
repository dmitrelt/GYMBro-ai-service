from fastapi import APIRouter, Depends
from app.schemas import NutritionRequest, NutritionResponse
from app.security import get_current_user
from app.llm import llm_client

router = APIRouter(
    prefix='/nutrition',
    tags=['nutrition']
)

@router.post('/calculate', response_model=NutritionResponse)
async def calculate_nutrition(
    request: NutritionRequest,
    user_id: int = Depends(get_current_user)
):
    """
    Fallback-ручка: когда Statistics Service не смог получить КБЖУ через Nutrition API,
    он отправляет сюда весь текст питания.
    """

    return NutritionResponse(
        success=False,
        items=[],
        error_message='Функция расчёта КБЖУ через нейросеть пока в разработке. '
                      'Пока Statistics Service не может передать сюда данные.'
    )
