# Imports
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    hashed_password = Column(String, index=True)
    access_code = Column(String, index=True)
    is_active = Column(Boolean, default=True)
    logs = relationship("Log", back_populates="owner")

class Log(Base):
    __tablename__ = "Logs"

    id = Column(Integer, primary_key=True, index=True)
    logName = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("Users.id"))

    owner = relationship("User", back_populates="logs")