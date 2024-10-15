from fastapi import Cookie, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from model.entities.ChatRoom import ChatRooms
from model.entities.Connection import Connections
from model.entities.User import Users
from model.some import get_db
from service.ConnectionManager import ConnectionManager
from service.UtilityFunctions import is_token_valid


class WebsocketService:
    async def handleWebsocket(self, websocket: WebSocket, name: str, manager: ConnectionManager, access_token: str = Cookie(None), db: Session = Depends(get_db)):
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
                all_users_in_chat = db.query(Connections).filter(Connections.id_chat_connection == is_chat_exist.id).all()
                list_of_ids = [buff_id.id for buff_id in all_users_in_chat]
                await manager.broadcast(f"Client {sender_info.email}: {data}", list_of_ids)
        except WebSocketDisconnect:
            manager.disconnect(websocket, sender_connection_info.id)
            db.delete(sender_connection_info)
            db.commit()
            await manager.broadcast(f"Client {sender_info.email} left the chat.", list_of_ids)