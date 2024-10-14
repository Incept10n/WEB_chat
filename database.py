from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from passlib.context import CryptContext

DATABASE_URL = "postgresql://chat:2143658790ADM+@localhost/webchat?options=-csearch_path%3Dmy_schema"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Users(Base):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'my_schema'}

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(150), unique=True, index=True, nullable=False)  
    passwd = Column(String(32), nullable=False)  

class ChatRooms(Base):  
    __tablename__ = 'chat_rooms'
    __table_args__ = {'schema': 'my_schema'}

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey('my_schema.users.id'), nullable=False)
    name = Column(String(50), nullable=False)

    owner = relationship("Users")

class Connections(Base):  
    __tablename__ = 'connections'
    __table_args__ = {'schema': 'my_schema'}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('my_schema.users.id'), nullable=False)
    id_chat_connection = Column(Integer, ForeignKey('my_schema.chat_rooms.id'), nullable=False)

    user = relationship("Users")
    chat_room = relationship("ChatRooms")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()