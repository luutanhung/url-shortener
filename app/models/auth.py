from pydantic import BaseModel, EmailStr, model_validator


class RegisterRequest(BaseModel):
    email: EmailStr
    username: str | None = None
    pwd: str

    @model_validator(mode="before")
    def set_username_if_missing(cls, values):
        if not values.get("username") and "email" in values:
            values["username"] = values["email"].split("@")[0]
        return values


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: str


class ChangePasswordRequest(BaseModel):
    old_pwd: str
    new_pwd: str
