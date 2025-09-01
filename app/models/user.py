from beanie import Document
from bson.objectid import ObjectId
from passlib.hash import bcrypt
from pydantic import BaseModel, EmailStr


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


class UserRead(BaseModel):
    id: str
    email: EmailStr
    username: str
