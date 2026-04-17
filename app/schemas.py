from pydantic import BaseModel, Field
from typing import List, Optional


class TrainingParseRequest(BaseModel):
    """
    Запрос от Bot-User Service на парсинг текста тренировки.
    """
    raw_text: str = Field(..., description='Свободный текст, который ввёл пользователь про всю тренировку')


class ExerciseSet(BaseModel):
    """
    Один подход в упражнении.
    """
    weight_kg: Optional[float] = Field(None, description='Вес в килограммах')
    reps: Optional[int] = Field(None, description='Количество повторений')
    duration_seconds: Optional[int] = Field(None, description='Время в секундах')
    distance_km: Optional[float] = Field(None, description='Дистанция в километрах')
    feeling: Optional[str] = Field(None, description='Субъективное ощущение')


class Exercise(BaseModel):
    """
    Одно упражнение, которое может содержать несколько подходов.
    """
    exercise_name: str = Field(..., description='Название упражнения')
    exercise_type: str = Field(..., description='Тип упражнения')
    muscle_group: Optional[str] = Field(None, description='Группа мышц')
    sets: List[ExerciseSet] = Field(..., description='Список подходов к этому упражнению')
    raw_input_text: Optional[str] = Field(None, description='Оригинальный текст')


class TrainingParseResponse(BaseModel):
    """
    Ответ AI Service после попытки распарсить тренировку.
    """
    success: bool = Field(..., description='Успешно ли прошёл парсинг')
    exercises: Optional[List[Exercise]] = Field(None, description='Список упражнений')
    error_message: Optional[str] = Field(None, description='Сообщение об ошибке, если парсинг не удался')


class NutritionRequest(BaseModel):
    """
    Запрос на fallback-расчёт КБЖУ через нейросеть.
    """
    raw_text: str = Field(..., description='Текст, который ввёл пользователь про питание')


class NutritionResponse(BaseModel):
    """
    Ответ с рассчитанным КБЖУ.
    """
    success: bool
    product_name: Optional[str] = None
    grams: Optional[float] = None
    calories: Optional[float] = None
    protein: Optional[float] = None
    fat: Optional[float] = None
    carbs: Optional[float] = None
    error_message: Optional[str] = None



class RecommendationRequest(BaseModel):
    """
    Запрос на генерацию персональной рекомендации.
    """
    goals_text: str
    restrictions_text: Optional[str] = None
    recent_workouts: Optional[str] = None
    recent_food: Optional[str] = None


class RecommendationResponse(BaseModel):
    """
    Ответ с рекомендацией от нейросети.
    """
    success: bool
    recommendation_text: str
    error_message: Optional[str] = None