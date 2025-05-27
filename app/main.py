from fastapi import FastAPI
from . import models
from .database import engine
from .routers import users, posts, auth, vote

models.Base.metadata.create_all(bind=engine)

#create an intstance of fastapi
app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)

#start the webserver using uvicorn = uvicorn main:app --reload (development env) uvicorn main:app(prod env)

    
