from fastapi import APIRouter, Depends

from app.models import User, UserRead

from .auth import get_current_user

router = APIRouter(prefix="/api/users")


@router.get("/profile", response_model=UserRead)
async def access_profile(user: User = Depends(get_current_user)):
    return UserRead(id=str(user.id), email=user.email, username=user.username)
