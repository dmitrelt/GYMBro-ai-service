from fastapi import APIRouter, Depends
from app.schemas import TrainingParseRequest, TrainingParseResponse
from app.security import get_current_user
from app.llm import llm_client

router = APIRouter(
    prefix='/training',
    tags=['training']
)

@router.post('/parse', response_model=TrainingParseResponse)
async def parse_training(
    request: TrainingParseRequest,
    user_id: int = Depends(get_current_user)
):
    """
    Основная ручка для парсинга свободного текста тренировки.
    """

    return TrainingParseResponse(
        success=False,
        exercises=None,
        error_message='Функция парсинга тренировок пока в разработке. '
                      'AI Service принимает запрос, но ещё не обрабатывает текст.'
    )
