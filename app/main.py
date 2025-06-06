from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import users, posts, auth, vote

# models.Base.metadata.create_all(bind=engine)

#create an intstance of fastapi
app = FastAPI()

origins = ["*"]
# Middleware to handle CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def hello():
    return {"message" :"Hello world!!!!"}

#start the webserver using uvicorn = uvicorn main:app --reload (development env) uvicorn main:app(prod env)

    
