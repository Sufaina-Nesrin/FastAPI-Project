from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import List, Annotated
from database import SessionLocal, engine
import models

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class PostBase(BaseModel):
    title: str
    context: str
    user_id: int

class UserBase(BaseModel):
    username: str

class UserReturn(UserBase):
    id: int

    class Config:
        orm_mode = True    

class PostReturn(PostBase):
    id: int

    class Config:
        orm_mode = True    

#dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
db_dependency = Annotated[SessionLocal, Depends(get_db)]      

# Create a new user
@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: db_dependency):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()

@app.get("/users/{user_id}", status_code=status.HTTP_200_OK)
async def get_user(user_id: int, db: db_dependency):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user    

@app.get("/users/", response_model=List[UserReturn], status_code=status.HTTP_200_OK)
async def get_users(db: db_dependency):
    users = db.query(models.User).all()
    return users

@app.post("/posts/", status_code=status.HTTP_201_CREATED)
async def create_post(post: PostBase, db: db_dependency):
    db_post = models.Post(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@app.get("/posts/{post_id}", status_code=status.HTTP_200_OK)
async def get_post(post_id: int, db: db_dependency):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@app.get("/posts/", response_model=List[PostReturn], status_code=status.HTTP_200_OK)
async def get_posts(db: db_dependency):
    posts = db.query(models.Post).all()
    return posts


@app.delete("/users/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(user_id: int, db: db_dependency):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    posts = db.query(models.Post).filter(models.Post.user_id == user_id).all()
    for post in posts:
        db.delete(post)

    db.delete(user)
    db.commit()
    return {"detail": "User and their posts deleted"}

@app.put("/users/{user_id}", response_model=UserReturn, status_code=status.HTTP_200_OK)
async def update_user(user_id: int, user: UserBase, db: db_dependency):
    user_to_update = db.query(models.User).filter(models.User.id == user_id).first()
    if user_to_update is None:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user.dict().items():
        setattr(user_to_update, key, value)
    db.commit()
    db.refresh(user_to_update)
    return user_to_update    
    
