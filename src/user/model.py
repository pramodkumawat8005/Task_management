from sqlalchemy import Column, Integer, String, Boolean
from src.utils.db import Base

class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    username = Column(String(100), nullable=False, unique=True)
    email = Column(String(200), nullable=False, unique=True)
    hashed_password = Column(String(200), nullable=False)
    is_active = Column(Boolean, default=True)