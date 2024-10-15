from fastapi import WebSocket

from model.entities.User import Users


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