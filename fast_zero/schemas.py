from pydantic import BaseModel


class Message(BaseModel):
    message: str


class HtmlResponse(BaseModel):
    html_content: str
