from datetime import datetime, timedelta, timezone

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.config import JWT_ALGORITHM, JWT_SECRET_KEY
from app.models import LoginRequest, RegisterRequest, Token, User, UserRead

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/jwt/login")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


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


router = APIRouter(prefix="/api/auth")


@router.post("/register", response_model=UserRead)
async def register(user: RegisterRequest):
    existing = await User.find_one(User.email == user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pwd = User.hash_pwd(user.pwd)
    user_doc = User(email=user.email, username=user.username, pwd=hashed_pwd)
    await user_doc.insert()
    return UserRead(
        id=str(user_doc.id), email=user_doc.email, username=user_doc.username
    )


@router.post("/jwt/login", response_model=Token)
async def login(data: LoginRequest):
    email: str = data.email
    pwd: str = data.pwd
    user = await User.find_one(User.email == email)
    if not user or not user.verify_pwd(pwd):
        raise HTTPException(status_code=404, detail="Invalid credentials")
    token = create_access_token({"sub": str(user.id)})
    return Token(access_token=token, token_type="bearer")
