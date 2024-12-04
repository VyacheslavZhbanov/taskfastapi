from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from models import Post, SessionLocal

app = FastAPI()


class PostCreate(BaseModel):
    title: str
    content: str


class PostResponse(BaseModel):
    id: int
    title: str
    content: str


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post(
        '/posts/',
         response_model=PostResponse,
         tags=['Posts'],
         summary='Create your post'
)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    db_post = Post(title=post.title, content=post.content)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    db.close()
    return db_post


@app.get(
        '/posts/',
         response_model=list[PostResponse],
         tags=['Posts'],
         summary='Show all posts'
)
def read_posts(db: Session = Depends(get_db)):
    posts = db.query(Post).all()
    db.close()
    return posts


@app.delete(
        '/posts/{post_id}',
        tags = ['Posts'],
        summary='Delete your post'
)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post is None:
        db.close()
        raise HTTPException(status_code=404, detail='Post not found')
    db.delete(post)
    db.commit()
    db.close()
    return {'detail': 'Post deleted'}

