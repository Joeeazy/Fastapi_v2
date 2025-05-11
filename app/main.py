from fastapi import FastAPI
from psycopg2.extras import RealDictCursor
import psycopg2
import time
from . import models
from .database import engine
from .routers import users, posts

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

app.include_router(posts.router)
app.include_router(users.router)

#start the webserver using uvicorn = uvicorn main:app --reload (development env) uvicorn main:app(prod env)

    
