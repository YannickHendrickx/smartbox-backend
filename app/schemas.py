# Imports
from pydantic import BaseModel

# Log schemas
class LogBase(BaseModel):
    logName: str

class LogAdd(LogBase):
    pass

class Log(LogBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

# User schemas
class userBase(BaseModel):
    name: str

class userAdd(userBase):
    password: str
    is_active: bool
    access_code: int

class user(userBase):
    id: int
    is_active: bool
    hashed_password: str
    access_code: int
    logs: list[Log] = []
    class Config:
        orm_mode = True