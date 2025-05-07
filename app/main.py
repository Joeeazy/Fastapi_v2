from fastapi import FastAPI, status, HTTPException, Response
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

#create an intstance of fastapi
app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = 0


#connection to postgres DB using psycopg2 library
while True:
    try:
        conn = psycopg2.connect(host = 'localhost', database = 'FastAPI_db', user = 'postgres', password = '123456', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection Successful")
        break
    except Exception as error:
        print("Connection to database failed")
        print("Error", error)
        time.sleep(2)


#store posts in memory variable array
my_posts = [
    {"title": "My 1st post", "content" : "contents to my 1st post", "id": 1}, 
    {"title": "My 2nd post", "content" : "contents to my 2nd post", "id": 2},
    {"title": "My 3rd post", "content" : "contents to my 3rd post", "id": 3}
]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_post_index(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i

#create a route = a decorator + a function logic
@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts():
    return {"items": my_posts}

@app.get("/posts/{id}")
def get_post_by_id(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} was not found")
    return {"item": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 100000)
    my_posts.append(post_dict)
    return {"items": post_dict}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    post = find_post_index(id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} was not found")
    my_posts.pop(post)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_post_index(id)

    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} was not found")

    post_dict = post.dict()

    post_dict["id"] = id

    my_posts[index] = post_dict

    return {"updated_post": my_posts}
    


# create post data expected = title str, content str

#start the webserver using uvicorn = uvicorn main:app --reload (development env) uvicorn main:app(prod env)
