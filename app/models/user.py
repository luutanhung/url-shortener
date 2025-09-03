from beanie import Document, PydanticObjectId
from bson.objectid import ObjectId
from passlib.hash import bcrypt
from pydantic import BaseModel, EmailStr, field_serializer


class User(Document):
    email: EmailStr
    username: str
    pwd: str
    is_active: bool = False

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
    is_active: bool

    @field_serializer("id")
    def serialize_id(self, id: PydanticObjectId, _info):
        return str(id)


class UserUpdate(BaseModel):
    username: str
