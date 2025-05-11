from fastapi import FastAPI, status, HTTPException, Response, Depends
from fastapi.params import Body
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from typing import List
import psycopg2
import time
from . import models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

#create an intstance of fastapi
app = FastAPI()

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

@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    #Raw Sql
    # cursor.execute(""" SELECT * FROM posts""")
    # posts = cursor.fetchall()
    #SqlAlchemy modified
    posts = db.query(models.Post).all()
    return posts

@app.get("/posts/{id}", response_model=schemas.Post)
def get_post_by_id(id: int, db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} was not found")
    return post


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (
    #     post.title, post.content, post.published))
    # new_post = cursor.fetchone()

    #new_post = models.Post(title = post.title, content = post.content, published = post.published)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # #sql command
    # cursor.execute("""DELETE FROM posts where id = %s RETURNING *""", (str(id),))
    # #fetch deleted post
    # deleted_post = cursor.fetchone()
    # #update db
    # conn.commit()

    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} was not found")

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()

    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} was not found")

    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return post_query.first()

#start the webserver using uvicorn = uvicorn main:app --reload (development env) uvicorn main:app(prod env)


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate,  db: Session = Depends(get_db)):
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
