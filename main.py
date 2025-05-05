from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
#create an intstance of fastapi
app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = 0

#create a route = a decorator + a function logic
@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    return {"data": "Your Post"}

@app.post("/createposts")
def create_posts(post: Post):
    print(post)
    print(post.dict())
    return {"items": post }


# create post data expected = title str, content str

#start the webserver using uvicorn = uvicorn main:app --reload (development env) uvicorn main:app(prod env)
