# Imports
from pydantic import BaseModel

# User schemas
class userBase(BaseModel):
    name: str

class userAdd(userBase):
    password: str

class user(userBase):
    id: int
    is_active: bool
    hashed_password: str

    class Config:
        orm_mode = True