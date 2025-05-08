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
    cursor.execute(""" SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"items": posts}

@app.get("/posts/{id}")
def get_post_by_id(id: int):
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} was not found")
    return {"item": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (
        post.title, post.content, post.published))

    new_post = cursor.fetchone()

    conn.commit()

    return {"items": new_post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    #sql command
    cursor.execute("""DELETE FROM posts where id = %s RETURNING *""", (str(id),))
    #fetch deleted post
    deleted_post = cursor.fetchone()
    #update db
    conn.commit()
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} was not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()

    conn.commit()

    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} was not found")

    return {"updated_post": updated_post}
    


# create post data expected = title str, content str

#start the webserver using uvicorn = uvicorn main:app --reload (development env) uvicorn main:app(prod env)
