from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import date


class TrainingParseRequest(BaseModel):
    """Запрос на парсинг свободного текста тренировки."""
    raw_text: str = Field(..., description="Свободный текст, который ввёл пользователь про всю тренировку")


class ExerciseSet(BaseModel):
    """Один подход в упражнении."""
    weight_kg: Optional[float] = Field(None, description="Вес в килограммах")
    reps: Optional[int] = Field(None, description="Количество повторений")
    duration_seconds: Optional[int] = Field(None, description="Время в секундах (для кардио)")
    distance_km: Optional[float] = Field(None, description="Дистанция в километрах")
    feeling: Optional[str] = Field(None, description="Субъективное ощущение")


class Exercise(BaseModel):
    """Одно упражнение."""
    exercise_name: str = Field(..., description="Название упражнения")
    exercise_type: str = Field(..., description="Тип упражнения (силовое, кардио, статика и т.д.)")
    muscle_group: Optional[str] = Field(None, description="Группа мышц")
    sets: List[ExerciseSet] = Field(..., description="Список подходов")
    raw_input_text: Optional[str] = Field(None, description="Оригинальный текст")


class TrainingParseResponse(BaseModel):
    """Ответ после парсинга тренировки."""
    success: bool
    exercises: Optional[List[Exercise]] = None
    error_message: Optional[str] = None



class NutritionRequest(BaseModel):
    """Запрос на расчёт КБЖУ через нейросеть."""
    raw_text: str = Field(..., description="Свободный текст питания от пользователя")


class NutritionItem(BaseModel):
    """Информация по одному продукту/блюду."""
    product_name: str
    grams: float
    calories: float
    protein: float
    fat: float
    carbs: float


class NutritionResponse(BaseModel):
    """Ответ после расчёта КБЖУ."""
    success: bool
    items: Optional[List[NutritionItem]] = None
    error_message: Optional[str] = None


class DailyWorkoutSummary(BaseModel):
    """Сводка по одной тренировке."""
    date: date
    exercises: List[str] = Field(..., description="Список названий упражнений в этот день")


class ExercisePeriodStats(BaseModel):
    """Детальная статистика по одному упражнению за период."""
    exercise_name: str
    muscle_group: Optional[str] = None
    total_sets: int
    avg_sets_per_workout: float
    max_weight_kg: Optional[float] = None
    avg_weight_kg: Optional[float] = None
    max_duration_seconds: Optional[int] = None
    avg_duration_seconds: Optional[float] = None
    max_distance_km: Optional[float] = None
    avg_distance_km: Optional[float] = None


class WorkoutPeriodStats(BaseModel):
    """Полная статистика тренировок за период."""
    start_date: date
    end_date: date
    period_days: int
    total_workouts: int
    exercise_stats: List[ExercisePeriodStats]
    daily_summaries: List[DailyWorkoutSummary]


class DailyNutritionSummary(BaseModel):
    """Суммарное КБЖУ за один день."""
    date: date
    calories: float
    protein: float
    fat: float
    carbs: float


class NutritionPeriodStats(BaseModel):
    """Полная статистика питания за период."""
    start_date: date
    end_date: date
    period_days: int
    avg_calories: float
    avg_protein: float
    avg_fat: float
    avg_carbs: float
    daily_summaries: List[DailyNutritionSummary]


class RecommendationRequest(BaseModel):
    """
    Запрос на генерацию персонализированной рекомендации.
    """
    goals_text: str = Field(..., description="Цели пользователя")
    restrictions_text: Optional[str] = Field(None, description="Ограничения, аллергены, травмы и т.д.")

    workouts: WorkoutPeriodStats
    nutrition: NutritionPeriodStats


class RecommendationResponse(BaseModel):
    """Ответ с рекомендацией от нейросети."""
    success: bool = True
    recommendation_text: str
    error_message: Optional[str] = None