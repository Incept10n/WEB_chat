from model.some import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

class ChatRooms(Base):  
    __tablename__ = 'chat_rooms'
    __table_args__ = {'schema': 'my_schema'}

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey('my_schema.users.id'), nullable=False)
    name = Column(String(50), nullable=False)

    owner = relationship("Users")