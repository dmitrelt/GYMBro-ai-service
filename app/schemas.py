from typing import List, Optional # noqa

from pydantic import BaseModel, Field


class TrainingParseRequest(BaseModel):
    """
    Запрос от Bot-User Service на парсинг текста тренировки.
    """
    raw_text: str = Field(..., description='Свободный текст, который ввёл пользователь про всю тренировку')


class ExerciseSet(BaseModel):
    """
    Один подход в упражнении.
    """
    weight_kg: float | None = Field(None, description='Вес в килограммах')
    reps: int | None = Field(None, description='Количество повторений')
    duration_seconds: int | None = Field(None, description='Время в секундах')
    distance_km: float | None = Field(None, description='Дистанция в километрах')
    feeling: str | None = Field(None, description='Субъективное ощущение')


class Exercise(BaseModel):
    """
    Одно упражнение, которое может содержать несколько подходов.
    """
    exercise_name: str = Field(..., description='Название упражнения')
    exercise_type: str = Field(..., description='Тип упражнения')
    muscle_group: str | None = Field(None, description='Группа мышц')
    sets: list[ExerciseSet] = Field(..., description='Список подходов к этому упражнению')
    raw_input_text: str | None = Field(None, description='Оригинальный текст')


class TrainingParseResponse(BaseModel):
    """
    Ответ AI Service после попытки распарсить тренировку.
    """
    success: bool = Field(..., description='Успешно ли прошёл парсинг')
    exercises: list[Exercise] | None = Field(None, description='Список упражнений')
    error_message: str | None = Field(None, description='Сообщение об ошибке, если парсинг не удался')


class NutritionRequest(BaseModel):
    """
    Запрос на fallback-расчёт КБЖУ через нейросеть.
    """
    raw_text: str = Field(..., description='Полный текст питания от пользователя')

class NutritionItem(BaseModel):
    """Информация по одному продукту"""
    product_name: str
    grams: float
    calories: float
    protein: float
    fat: float
    carbs: float

class NutritionResponse(BaseModel):
    """
    Ответ от нейросети с расчётом КБЖУ для всех продуктов.
    """
    success: bool
    items: list[NutritionItem] | None = Field(None, description='Список рассчитанных продуктов')
    error_message: str | None = Field(None, description='Подробное сообщение, если не удалось обработать')


class RecommendationRequest(BaseModel):
    """
    Запрос на генерацию персональной рекомендации.
    """
    goals_text: str
    restrictions_text: str | None = None
    recent_workouts: str | None = None
    recent_food: str | None = None


class RecommendationResponse(BaseModel):
    """
    Ответ с рекомендацией от нейросети.
    """
    success: bool
    recommendation_text: str
    error_message: str | None = None
