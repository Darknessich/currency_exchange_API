from fastapi import APIRouter, Depends, HTTPException, status

import app.utils.external_api as api
from app.api.models.currency import Convert
from app.core.security import get_user_from_token
from app.repositories.user_repository import UserRepository, get_user_repository

router = APIRouter(prefix="/currency")


@router.get("/convert")
async def convert(
    query: Convert,
    user: str = Depends(get_user_from_token),
    repo: UserRepository = Depends(get_user_repository),
) -> Convert:
    if not await repo.get_user(user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="access is denied"
        )
    return await api.convert(query)
