from fastapi import Cookie, Depends
from model.entities.ChatRoom import ChatRooms
from model.some import get_db
from schema import Chat_room
from service.UtilityFunctions import is_token_valid
from sqlalchemy.orm import Session


class ChatService:
    def createChat(self, chat: Chat_room, access_token: str = Cookie(None), db: Session = Depends(get_db)):
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

    def deleteChat(self, chat: Chat_room, access_token: str = Cookie(None), db: Session = Depends(get_db)):
        if is_token_valid(access_token):
        # check the length of valid name
            existing_chat = db.query(ChatRooms).filter(ChatRooms.name == chat.name, ChatRooms.owner_id == is_token_valid(access_token)).first()
            if existing_chat:
                db.delete(existing_chat)
                db.commit()
                return {"message": "Chat deleted successfully"}
            else:
                return {"error": "Chat not found or you do not have permission to delete it"}

    def getChats(self, sequence: str = None, db: Session = Depends(get_db)):
        if sequence is None:
            rooms = db.query(ChatRooms).all()
        else:
            rooms = db.query(ChatRooms).filter(ChatRooms.name.ilike(f"%{sequence}%")).all()
            return {"rooms": [room.name for room in rooms]}                
                
