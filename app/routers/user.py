from typing import List
from fastapi import HTTPException, status, Depends, APIRouter

from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(userCreate: schemas.UserCreate, db: Session = Depends(get_db)):
    
    userCreate.password = utils.hash_pwd(userCreate.password)

    user = models.User(**userCreate.dict())
    db.add(user)
    db.commit()
    db.refresh(user)

    return user

@router.get("/{id}", response_model=schemas.UserResponse)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter_by(id = id).first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"User with id {id} not found")

    return user