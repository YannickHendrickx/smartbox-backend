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

class userPatch(BaseModel):
    is_active: bool
    access_code: str

class userAdd(userBase):
    password: str

class user(userBase):
    id: int
    is_active: bool
    hashed_password: str
    access_code: str
    logs: list[Log] = []
    class Config:
        orm_mode = True