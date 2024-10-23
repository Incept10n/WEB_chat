from fastapi import Cookie, Depends, FastAPI, Response
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from fastapi import Response
from fastapi.staticfiles import StaticFiles
from model.some import get_db
from schema import Chat_room, Login, Register
from service.services.ChatService import ChatService
from service.services.AuthenticationService import AuthenticationService

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

authenticationService = AuthenticationService()
chatService = ChatService()

@app.get("/")
async def get():
    return FileResponse("static/index.html")

@app.post("/register")
async def register(user: Register, db: Session = Depends(get_db)):
    return authenticationService.register(user, db)

@app.post("/login")
async def login(user: Login, response: Response, db: Session = Depends(get_db)):
    return authenticationService.login(user, response, db)

@app.post("/create_chat")
async def create_chat(chat: Chat_room, access_token: str = Cookie(None), db: Session = Depends(get_db)):
    return chatService.createChat(chat, access_token, db)

@app.post("/delete_chat")
async def delete_chat(chat: Chat_room, access_token: str = Cookie(None), db: Session = Depends(get_db)):
    return chatService.deleteChat(chat, access_token, db)

@app.get("/chat_rooms/")
async def get_chat_rooms(sequence: str = None, db: Session = Depends(get_db)):
    return chatService.getChats(sequence, db)

@app.get("/owner_chat_rooms")
async def get_owner_chat_rooms(access_token: str = Cookie(None), db: Session = Depends(get_db)):
    return chatService.getOwnerChat(access_token, db)

@app.get("/is_chat_exist")
async def is_chat_exist(name: str, db: Session = Depends(get_db)):
    return chatService.isChatExist(name, db)