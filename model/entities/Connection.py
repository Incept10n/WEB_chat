from model.some import Base
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

class Connections(Base):  
    __tablename__ = 'connections'
    __table_args__ = {'schema': 'my_schema'}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('my_schema.users.id'), nullable=False)
    id_chat_connection = Column(Integer, ForeignKey('my_schema.chat_rooms.id'), nullable=False)

    user = relationship("Users")
    chat_room = relationship("ChatRooms")