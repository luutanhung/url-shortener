from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from app.models.user import User, UserCreate, UserRead
from app.schemas import LoginRequest

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if not credentials:
            raise HTTPException(status_code=403, detail="Invalid authorization code")
        try:
            payload = decode_access_token(credentials.credentials)
            return payload
        except JWTError:
            raise HTTPException(status_code=403, detail="Invalid token")


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(hours=1))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


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


@router.post("/jwt/login")
async def login(data: LoginRequest):
    email: str = data.email
    pwd: str = data.pwd
    user = await User.find_one(User.email == email)
    if not user or not user.verify_pwd(pwd):
        raise HTTPException(status_code=404, detail="Invalid credentials")
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", dependencies=[Depends(JWTBearer())], response_model=UserRead)
async def get_me(user_data=Depends(JWTBearer())):
    user_id = user_data["sub"]
    user = await User.get(user_id)
    return UserRead(id=str(user.id), email=user.email, username=user.username)
