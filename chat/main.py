from fastapi import Cookie, Depends, FastAPI, WebSocket
from sqlalchemy.orm import Session
from model.some import get_db
from service.ConnectionManager import ConnectionManager
from service.services.WebsocketService import WebsocketService    

app = FastAPI()

manager = ConnectionManager()
websocketService = WebsocketService()

@app.websocket("/ws/{name}")
async def websocket_endpoint(websocket: WebSocket, name: str, access_token: str = Cookie(None), db: Session = Depends(get_db)):
    await websocketService.handleWebsocket(websocket, name, manager, access_token, db)