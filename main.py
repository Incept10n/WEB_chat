from fastapi import Cookie, Depends, FastAPI, WebSocket, Response
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from fastapi import Response
from fastapi.staticfiles import StaticFiles
from model.some import get_db
from schema import Chat_room, Login, Register
from service.ConnectionManager import ConnectionManager
from service.services.ChatService import ChatService
from service.services.AuthenticationService import AuthenticationService
from service.services.WebsocketService import WebsocketService    

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

manager = ConnectionManager()
authenticationService = AuthenticationService()
chatService = ChatService()
websocketService = WebsocketService()

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

@app.websocket("/ws/{name}")
async def websocket_endpoint(websocket: WebSocket, name: str, access_token: str = Cookie(None), db: Session = Depends(get_db)):
    await websocketService.handleWebsocket(websocket, name, manager, access_token, db)