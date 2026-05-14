from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> int:
    """Заглушка авторизации для разработки и лабораторных"""
    if not credentials or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не предоставлен токен",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Для тестов возвращаем фиксированный user_id
    fake_user_id = 1
    print(f"[AI Service] Запрос обработан для user_id={fake_user_id}")
    return fake_user_id