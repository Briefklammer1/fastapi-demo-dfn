from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import oauth2
from .. import database, schemas, models, utils

router = APIRouter(tags=["auth"])

@router.post("/login", response_model=schemas.Token)
def login(userLogin: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    user = db.query(models.User).filter(models.User.email == userLogin.username).first()
    # here username can be anything, its just a name, here username is actually email
    if not user:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Invalid Credentials...")

    if not utils.verify_pwd(pwd_plain=userLogin.password, pwd_hashed=user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials...")

    access_token = oauth2.create_access_token(data={"user_id": user.id})
    print(f"Logged in with user_id: {user.id}")

    return {"access_token": access_token, "token_type": "bearer"}