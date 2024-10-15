from fastapi import Cookie, Depends, FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Response
from fastapi.responses import FileResponse
from model.entities.ChatRoom import ChatRooms
from model.entities.Connection import Connections
from model.entities.User import Users
from sqlalchemy.orm import Session
from fastapi import Response
from fastapi.staticfiles import StaticFiles
from model.some import get_db
from schema import Chat_room, Login, Register
from service.ConnectionManager import ConnectionManager
from service.UtilityFunctions import create_access_token, hash_sha256, is_token_valid
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
    # return FileResponse("static/chat.html")
    return FileResponse("static/index.html")

@app.post("/register")
#check uniquness of email 
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
    return chatService.createChat(chat, access_token, db)

@app.get("/chat_rooms/")
async def get_chat_rooms(sequence: str = None, db: Session = Depends(get_db)):
    return chatService.getChats(sequence, db)

@app.websocket("/ws/{name}")
async def websocket_endpoint(websocket: WebSocket, name: str, access_token: str = Cookie(None), db: Session = Depends(get_db)):
    await websocketService.handleWebsocket(websocket, name, manager, access_token, db)