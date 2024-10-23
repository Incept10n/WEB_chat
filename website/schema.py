from pydantic import BaseModel

class Login(BaseModel):
    email: str
    passwd: str

class Register(BaseModel):
    email: str
    passwd: str

class Chat_room(BaseModel):
    name: str
