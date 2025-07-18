
from sqlalchemy import Boolean, Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    # email = Column(String, unique=True, index=True)
    # full_name = Column(String, index=True)
    # disabled = Column(Boolean, default=False)

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String )
    code = Column(String,unique=True, index=True)
    user_id = Column(Integer)