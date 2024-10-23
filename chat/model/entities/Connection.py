from model.some import Base
from sqlalchemy import Column, Integer

class Connections(Base):  
    __tablename__ = 'connections'
    __table_args__ = {'schema': 'my_schema'}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer,  nullable=False)
    id_chat_connection = Column(Integer,  nullable=False)