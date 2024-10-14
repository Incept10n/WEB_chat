from fastapi import Cookie, Depends, FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Response
from fastapi.responses import FileResponse
from schema import Login, Register, Chat_room
from database import Users, ChatRooms, Connections, get_db
from sqlalchemy.orm import Session
import hashlib
from fastapi import Response

import jwt
from datetime import datetime, timedelta, timezone
from fastapi.staticfiles import StaticFiles    



app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


SECRET_KEY = "hehehihihaha"  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def hash_sha256(data: str) -> str:
    sha256_hash = hashlib.sha256()
    sha256_hash.update(data.encode('utf-8'))
    return sha256_hash.hexdigest()

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def is_token_valid(access_token):
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=403, detail="Token is invalid")

    user_id = payload.get("user_id")
    if user_id is None:
        raise HTTPException(status_code=403, detail="Token does not contain user_id")

    return user_id

class ConnectionManager:
    def __init__(self):
        self.connections: dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, sender_info: Users, list_of_ids: list, id_of_connection: int):
        await websocket.accept()
        self.connections[id_of_connection] = websocket
        await self.broadcast(f"Client {sender_info.email} joined the chat.", list_of_ids)

    def disconnect(self, websocket: WebSocket, id_of_connection: int):
        del self.connections[id_of_connection]

    async def broadcast(self, message: str, list_of_ids: list):
        for id, connection in self.connections.items():
            if id in list_of_ids:
                await connection.send_text(message)

manager = ConnectionManager()

@app.get("/")
async def get():
    # return FileResponse("static/chat.html")
    return FileResponse("static/index.html")

@app.post("/register")
#check uniquness of email 
async def register(user: Register, db: Session = Depends(get_db)):
    db_user = db.query(Users).filter(Users.email == user.email).first()
    if (db_user):
        raise HTTPException(status_code = 401, detail="Username already registered")
    new_user = Users(email=user.email, passwd=hash_sha256(user.passwd))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Users registered successfully"}

@app.post("/login")
async def login(user: Login, response: Response, db: Session = Depends(get_db)):
    db_user = db.query(Users).filter(Users.email == user.email, Users.passwd == hash_sha256(user.passwd)).first()
    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
        )
    access_token = create_access_token(data={
        "user_id": db_user.id,
        "email": user.email
        })

    response.set_cookie(key="access_token", value=access_token.decode('utf-8'), httponly=True)
    return {"access_token": access_token}

@app.post("/create_chat")
async def create_chat(chat: Chat_room, access_token: str = Cookie(None), db: Session = Depends(get_db)):
    if is_token_valid(access_token):
        # check the length of valid name
        # check for the same name of the chat
        new_chat = ChatRooms(owner_id=is_token_valid(access_token), name=chat.name) 
        db.add(new_chat)
        db.commit()
        db.refresh(new_chat)
        return {"message": "Chat created succsessfuly"}
    else:
        return {"error": "You do not have permission to create it"}    
    
@app.post("/delete_chat")
async def delete_chat(chat: Chat_room, access_token: str = Cookie(None), db: Session = Depends(get_db)):
    if is_token_valid(access_token):
        # check the length of valid name
        existing_chat = db.query(ChatRooms).filter(ChatRooms.name == chat.name, ChatRooms.owner_id == is_token_valid(access_token)).first()
        if existing_chat:
            db.delete(existing_chat)
            db.commit()
            return {"message": "Chat deleted successfully"}
        else:
            return {"error": "Chat not found or you do not have permission to delete it"}

@app.get("/chat_rooms/")
async def get_chat_rooms(sequence: str = None, db: Session = Depends(get_db)):
    if sequence is None:
        rooms = db.query(ChatRooms).all()
    else:
        rooms = db.query(ChatRooms).filter(ChatRooms.name.ilike(f"%{sequence}%")).all()
    return {"rooms": [room.name for room in rooms]}

@app.websocket("/ws/{name}")
async def websocket_endpoint(websocket: WebSocket, name: str, access_token: str = Cookie(None), db: Session = Depends(get_db)):
    if is_token_valid(access_token):
        sender_id = is_token_valid(access_token)
        is_chat_exist = db.query(ChatRooms).filter(ChatRooms.name == name).first()
        if is_chat_exist:
            new_connection = Connections(user_id=sender_id, id_chat_connection=is_chat_exist.id)
            db.add(new_connection)
            db.commit()
            db.refresh(new_connection)
            
            sender_info = db.query(Users).filter(Users.id == sender_id).first()
            sender_connection_info = db.query(Connections).filter(Connections.user_id == sender_id, Connections.id_chat_connection == is_chat_exist.id).first()
            all_users_in_chat = db.query(Connections).filter(Connections.id_chat_connection == is_chat_exist.id).all()
            list_of_ids = [buff_id.id for buff_id in all_users_in_chat]
            await manager.connect(websocket, sender_info, list_of_ids, sender_connection_info.id)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Client {sender_info.email}: {data}", list_of_ids)
    except WebSocketDisconnect:
        manager.disconnect(websocket, sender_connection_info.id)
        await manager.broadcast(f"Client {sender_info.email} left the chat.", list_of_ids)


