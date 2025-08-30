from fastapi import APIRouter, HTTPException
from app.models.user import User, UserRead, UserCreate

router = APIRouter(prefix="/auth")


@router.post("/register", response_model=UserRead)
async def register(user: UserCreate):
    existing = await User.find_one(User.email == user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pwd = User.hash_pwd(user.pwd)
    user_doc = User(email=user.email, username=user.username, pwd=hashed_pwd)
    await user_doc.insert()
    return UserRead(
        id=str(user_doc.id), email=user_doc.email, username=user_doc.username
    )
