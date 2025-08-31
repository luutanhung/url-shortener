from beanie import Document
from bson.objectid import ObjectId
from passlib.hash import bcrypt
from pydantic import BaseModel, EmailStr, model_validator


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
    username: str | None = None
    pwd: str

    @model_validator(mode="before")
    def set_username_if_missing(cls, values):
        if not values.get("username") and "email" in values:
            values["username"] = values["email"].split("@")[0]
        return values


class UserRead(BaseModel):
    id: str
    email: EmailStr
    username: str
