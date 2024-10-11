from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from typing import List

app = FastAPI()

class ConnectionManager:
    def __init__(self):
        # self.connections: List[WebSocket] = []
        self.connections: dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        # self.connections.append(websocket)
        self.connections[client_id] = websocket
        await self.broadcast(f"Client {client_id} joined the chat.", client_id)

    def disconnect(self, websocket: WebSocket, client_id: str):
        # self.connections.remove(websocket)
        del self.connections[client_id]

    async def broadcast(self, message: str, sender_id: str = None):
        # for connection in self.connections:
        #     await connection.send_text(message)
        for connection in self.connections.values():
            await connection.send_text(message)

manager = ConnectionManager()

@app.get("/")
async def get():
    return FileResponse("static/chat.html")

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)

    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Client {client_id}: {data}", client_id)
    except WebSocketDisconnect:
        manager.disconnect(websocket, client_id)
        await manager.broadcast(f"Client {client_id} left the chat.", client_id)
