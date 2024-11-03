from fastapi import Cookie, Depends, WebSocket, WebSocketDisconnect, HTTPException
from sqlalchemy.orm import Session

from model.entities.Connection import Connections
from model.some import get_db
from service.ConnectionManager import ConnectionManager
from service.UtilityFunctions import is_chat_exist, is_token_valid


class WebsocketService:
    async def handleWebsocket(self, websocket: WebSocket, name: str, manager: ConnectionManager, access_token: str = Cookie(None), db: Session = Depends(get_db)):
        try:
            sender_id, sender_email = is_token_valid(access_token)
            if sender_email:
                idOfChat = is_chat_exist(name)
                if idOfChat:
                    new_connection = Connections(user_id=sender_id, id_chat_connection=idOfChat)
                    db.add(new_connection)
                    db.commit()
                    db.refresh(new_connection)

                    sender_connection_info = db.query(Connections).filter(Connections.user_id == sender_id, Connections.id_chat_connection == idOfChat).first()
                    all_users_in_chat = db.query(Connections).filter(Connections.id_chat_connection == idOfChat).all()
                    list_of_ids = [buff_id.id for buff_id in all_users_in_chat]
                    await manager.connect(websocket, sender_email, list_of_ids, sender_connection_info.id)
            else:
                raise HTTPException(status_code=403, detail="token is not valid")
        except Exception as e:
            print(f"Unexpected error: {e}")
            await websocket.close(code=403, reason="Unexpected error occurred")
        try:
            while True:
                data = await websocket.receive_text()
                all_users_in_chat = db.query(Connections).filter(Connections.id_chat_connection == idOfChat).all()
                list_of_ids = [buff_id.id for buff_id in all_users_in_chat]
                await manager.broadcast(f"Client {sender_email}: {data}", list_of_ids)
        except WebSocketDisconnect:
            manager.disconnect(websocket, sender_connection_info.id)
            db.delete(sender_connection_info)
            db.commit()
            await manager.broadcast(f"Client {sender_email} left the chat.", list_of_ids)