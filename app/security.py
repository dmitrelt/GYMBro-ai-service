from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer

security = HTTPBearer()

async def get_current_user(credentials: HTTPBearer = Depends(security)) -> int:
    fake_user_id = 1

    return fake_user_id