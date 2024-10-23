from pydantic import BaseModel

class Chat_room(BaseModel):
    name: str

class Connection(BaseModel):
    user_id: int
    id_chat_connection: int