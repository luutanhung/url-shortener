from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.config import (
    JWT_ALGORITHM,
    JWT_EMAIL_ACTIVATION_EXPIRE_MINUTES,
    JWT_SECRET_KEY,
)
from app.models import (
    ChangePasswordRequest,
    RegisterRequest,
    ResponseModel,
    User,
    UserRead,
)
from app.utils.email import send_activation_email

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/jwt/login")
oauth2_schema_optional = OAuth2PasswordBearer(
    tokenUrl="/api/auth/jwt/login", auto_error=False
)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(days=3))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def create_activation_token(email: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=JWT_EMAIL_ACTIVATION_EXPIRE_MINUTES
    )
    payload = {"sub": email, "exp": expire}
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    user = await User.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )
    return user


async def get_current_user_optional(
    token: Optional[str] = Depends(oauth2_schema_optional),
) -> Optional[User]:
    if not token:
        return None
    try:
        return await get_current_user(token)
    except Exception:
        return None


router = APIRouter(prefix="/api/auth")


@router.post("/register", response_model=UserRead)
async def register(
    user: RegisterRequest, request: Request, background_tasks: BackgroundTasks
):
    existing = await User.find_one(User.email == user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pwd = User.hash_pwd(user.pwd)
    user_doc = User(email=user.email, username=user.username, pwd=hashed_pwd)
    await user_doc.insert()

    token: str = create_activation_token(user.email)
    base_url: str = str(request.base_url).rstrip("/")
    activation_link: str = f"{base_url}/api/auth/activate?token={token}"
    background_tasks.add_task(send_activation_email, user.email, activation_link)
    return UserRead(
        id=str(user_doc.id), email=user_doc.email, username=user_doc.username
    )


@router.get("/activate")
async def activate(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=400, detail="Invalid token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=400, detail="Invalid token")

    user = await User.find_one(User.email == email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.is_active:
        return {"message": "Account already activated"}

    user.is_active = True
    await user.save()

    return {"message": "Account activated successfully"}


@router.post("/jwt/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    email: str = form_data.username
    pwd: str = form_data.password
    user = await User.find_one(User.email == email)
    if not user or not user.verify_pwd(pwd):
        raise HTTPException(status_code=404, detail="Invalid credentials")

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account not activated. Please check your email to activate your account.",
        )

    token = create_access_token({"sub": str(user.id)})
    return {
        "access_token": token,
        "token_type": "Bearer",
        "user": UserRead(
            id=str(user.id),
            email=user.email,
            username=user.username,
            is_active=user.is_active,
        ).model_dump(),
    }


@router.post("/change-password", response_model=ResponseModel)
async def change_password(
    data: ChangePasswordRequest, user: User = Depends(get_current_user)
):
    if not user.verify_pwd(data.old_pwd):
        raise HTTPException(status_code=400, detail="Old password is incorrect")

    user.pwd = User.hash_pwd(data.new_pwd)
    await user.save()
    return ResponseModel(success=True, message="Password changed successfully")
