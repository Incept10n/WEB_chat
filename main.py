from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from typing import List

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <input type="text" id="messageText" autocomplete="off"/>
        <button onclick="sendMessage()">Send</button>
        <ul id='messages'>
        </ul>
        <script>
            const clientId = prompt("Enter your client ID:");
            const ws = new WebSocket(`ws://localhost:8000/ws/${clientId}`);
            
            ws.onmessage = function(event) {
                const messages = document.getElementById('messages');
                const message = document.createElement('li');
                const content = document.createTextNode(event.data);
                message.appendChild(content);
                messages.appendChild(message);
            };

            function sendMessage() {
                const input = document.getElementById("messageText");
                ws.send(input.value);
                input.value = '';
            }
        </script>
    </body>
</html>
"""

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
    return HTMLResponse(html)

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
