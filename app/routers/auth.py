from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags=["Authnetication"])

@router.post("/login", response_model=schemas.Token)
def login(user_credentials: schemas.UserLogin, db: Session = Depends(database.get_db)):

    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()

    if user == None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    #create a token
    access_token = oauth2.create_access_token(data = {"user_id": user.id, "user_email": user.email})
    #return a token
    return {"access_token": access_token, "token_type": "bearer"}

