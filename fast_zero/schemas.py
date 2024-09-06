from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    message: str


class HtmlResponse(BaseModel):
    html_content: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr


class UserDB(UserSchema):
    id: int


class UserList(BaseModel):
    users: list[UserPublic]
