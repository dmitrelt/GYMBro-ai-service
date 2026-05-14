# app/security.py
from fastapi import Depends


async def get_current_user() -> int:
    """
    Простая заглушка авторизации для разработки и тестирования.
    Не требует токен.
    """
    fake_user_id = 1
    return fake_user_id