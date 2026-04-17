from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.training import router as training_router
from app.routers.nutrition import router as nutrition_router
from app.routers.recommendation import router as recommendation_router


app = FastAPI(
    title='GYMBro AI service',
    description='Сервис для парсинга тренировок, расчёта КБЖУ и генерации рекомендаций с помощью нейросети',
    version='0.1.0',
    docs_url='/docs',
    redoc_url='/redoc'
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


app.include_router(training_router)
app.include_router(nutrition_router)
app.include_router(recommendation_router)


@app.get('/')
async def root():
    """
    Корневая ручка. Показывает, что сервис работает.
    """
    return {
        'message': 'AI Service is running',
        'status': 'ok',
        'version': '0.1.0',
        'documentation': '/docs'
    }
