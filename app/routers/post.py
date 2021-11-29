from typing import List, Optional
from fastapi import HTTPException, Response, status, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.sql import functions as fn
from sqlalchemy.sql.expression import label
from starlette.status import HTTP_401_UNAUTHORIZED
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(prefix="/posts", tags=["posts"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(postCreate: schemas.PostCreate,
                db: Session = Depends(get_db),
                current_user: models.User = Depends(oauth2.get_current_user)):

    post = models.Post(creator_id=current_user.id, **postCreate.dict())
    db.add(post)
    db.commit()
    db.refresh(post)

    return post


@router.get("/", response_model=List[schemas.PostGet])
def get_all_posts(db: Session = Depends(get_db),
                  search: Optional[str] = "",
                  limit: int = 10,
                  skip : int = 0):

    posts = db.query(models.Post, fn.count(models.Vote.post_id).label("votes")) \
              .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True) \
              .group_by(models.Post.id) \
              .filter(models.Post.title.contains(search)) \
              .limit(limit) \
              .offset(skip) \
              .all()

    return posts


@router.get("/{id}", response_model=schemas.PostGet)
def get_post_by_id(id: int,
                   db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id).first()

    vote_count = db.query(fn.count("*").label("vote_count")).filter(models.Vote.post_id == id).first()[0]
    print(vote_count)

    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Post with id {id} not found")

    return {"Post": post, "votes": vote_count}


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post_by_id(id: int,
                      db: Session = Depends(get_db), 
                      current_user: models.User = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Post with id {id} not found")
    if post.creator_id != current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, f"You are not allowed to delete the post with id {id}!")
    
    post_query.delete()
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post_by_id(id: int,
                      postUpdate: schemas.PostUpdate,
                      db: Session = Depends(get_db),
                      current_user: models.User = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Post with id {id} not found")
    if post.creator_id != current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, f"You are not allowed to change the post with id {id}!")
    post_query.update(postUpdate.dict())
    db.commit()
    db.refresh(post)

    return post