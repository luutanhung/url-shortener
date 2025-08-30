from beanie import Document
from pydantic import BaseModel, EmailStr
from passlib.hash import bcrypt
from bson.objectid import ObjectId


class User(Document):
    email: EmailStr
    username: str
    pwd: str
    is_active: bool = True

    class Settings:
        name = "users"

    model_config = {"json_encoders": {ObjectId: str}}

    def verify_pwd(self, pwd: str) -> bool:
        return bcrypt.verify(pwd, self.pwd)

    @classmethod
    def hash_pwd(cls, pwd: str) -> str:
        return bcrypt.hash(pwd)


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    pwd: str


class UserRead(BaseModel):
    id: str
    email: EmailStr
    username: str
