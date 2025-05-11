from pydantic import BaseModel, EmailStr
from datetime import datetime
#pydantic schema validation

#Request model
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

#response model
class Post(PostBase):
    id: int
    created_at: datetime   

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: str
    created_at: datetime