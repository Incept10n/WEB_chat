from pydantic import BaseModel

class Login(BaseModel):
    email: str
    passwd: str

class Register(BaseModel):
    email: str
    passwd: str

class Chat_room(BaseModel):
    name: str

class Connection(BaseModel):
    user_id: int
    id_chat_connection: int