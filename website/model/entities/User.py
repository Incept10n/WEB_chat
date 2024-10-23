from model.some import Base
from sqlalchemy import Column, Integer, String

class Users(Base):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'my_schema'}

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(150), unique=True, index=True, nullable=False)  
    passwd = Column(String(64), nullable=False)  