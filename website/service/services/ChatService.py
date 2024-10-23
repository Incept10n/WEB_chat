from fastapi import Cookie, Depends, HTTPException
from model.entities.ChatRoom import ChatRooms
from model.some import get_db
from schema import Chat_room
from service.UtilityFunctions import is_token_valid
from sqlalchemy.orm import Session


class ChatService:
    def createChat(self, chat: Chat_room, access_token: str = Cookie(None), db: Session = Depends(get_db)):
        if (len(chat.name) < 5):
            raise HTTPException(status_code=403, detail="The name of the chat is too short. Make it at least 6 symbols")  

        isChatAlreadyExist = db.query(ChatRooms).filter(ChatRooms.name == chat.name).first()

        if (isChatAlreadyExist):
            raise HTTPException(status_code=403, detail="This name of the chat already exist") 

        if (is_token_valid(access_token)):
            new_chat = ChatRooms(owner_id=is_token_valid(access_token), name=chat.name) 
            db.add(new_chat)
            db.commit()
            db.refresh(new_chat)
            return {"message": "Chat created succsessfuly"}
        else:
            raise HTTPException(status_code=403, detail="You do not have permission to create it")

    def deleteChat(self, chat: Chat_room, access_token: str = Cookie(None), db: Session = Depends(get_db)):
        if is_token_valid(access_token):
            existing_chat = db.query(ChatRooms).filter(ChatRooms.name == chat.name, ChatRooms.owner_id == is_token_valid(access_token)).first()
            if existing_chat:
                db.delete(existing_chat)
                db.commit()
                return {"message": "Chat deleted successfully"}
            else:
                raise HTTPException(status_code=401, detail="Chat not found or you do not have permission to delete it")

    def getChats(self, sequence: str = None, db: Session = Depends(get_db)):
        if sequence is None:
            rooms = db.query(ChatRooms).all()
        else:
            rooms = db.query(ChatRooms).filter(ChatRooms.name.ilike(f"%{sequence}%")).all()
        return {"rooms": [room.name for room in rooms]}                

    def getOwnerChat(self, access_token: str = Cookie(None) , db: Session = Depends(get_db)):
        user_id = is_token_valid(access_token)
        if user_id:
            ownerRooms = db.query(ChatRooms).filter(ChatRooms.owner_id == user_id).all()
            return {"owner_rooms": [owner_room.name for owner_room in ownerRooms]}
        raise HTTPException(status_code=401, detail="Invalid token")

    def isChatExist(self, name: str, db: Session = Depends(get_db)):
        searchChatResult = db.query(ChatRooms).filter(ChatRooms.name == name).first()
        if searchChatResult:
            return searchChatResult.id
        else:
            raise HTTPException(status_code=404, detail="The chat does not exist")
        

                
