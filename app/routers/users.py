from fastapi import APIRouter, Depends

from app.exceptions import UsernameAlreadyTaken
from app.models import User, UserRead, UserUpdate

from .auth import get_current_user

router = APIRouter(prefix="/api/users")


@router.get("/profile", response_model=UserRead)
async def access_profile(user: User = Depends(get_current_user)):
    return UserRead(
        id=str(user.id),
        email=user.email,
        username=user.username,
        is_active=user.is_active,
    )


@router.put("/profile", response_model=UserRead)
async def update_profile(data: UserUpdate, user: User = Depends(get_current_user)):
    username: str = data.username

    existing_user = await User.find_one(User.username == username)
    if existing_user and existing_user.id != user.id:
        raise UsernameAlreadyTaken(username)

    user.username = username
    await user.save()

    return UserRead(
        id=str(user.id),
        email=user.email,
        username=user.username,
        is_active=user.is_active,
    )
