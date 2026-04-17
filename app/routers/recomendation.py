from fastapi import APIRouter, Depends
from app.schemas import RecommendationRequest, RecommendationResponse
from app.security import get_current_user

router = APIRouter(
    prefix='/recommendation',
    tags=['recommendation']
)

@router.post('/', response_model=RecommendationResponse)
async def generate_recommendation(
    request: RecommendationRequest,
    user_id: int = Depends(get_current_user)
):
    """
    Ручка для генерации персонализированной рекомендации.
    """

    return RecommendationResponse(
        success=True,
        recommendation_text='Персональная рекомендация от нейросети пока в разработке.\n'
                            'Скоро здесь будет умный совет на основе твоих целей, '
                            'ограничений и истории тренировок/питания.',
        error_message=None
    )
