from pydantic import BaseModel, Field


class UserLogin(BaseModel):
    username: str = Field(pattern="^[a-zA-Z0-9_-]{5,32}$")
    password: str


class User(UserLogin):
    id: int
    salt: str
