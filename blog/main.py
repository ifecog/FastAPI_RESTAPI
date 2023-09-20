from fastapi import FastAPI, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session

from . import models

from .database import engine, SessionLocal 
from .schemas import Blog


app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

models.Base.metadata.create_all(bind=engine)

@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create_blog(request: Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(
        title=request.title,
        body=request.body
    )
    
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    
    return new_blog

@app.get('/blog')
def get_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    
    return blogs

@app.get('/blog/{id}', status_code=status.HTTP_200_OK)
def get_blog_by_id(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with the id of {id} not found!')
        # response.status_code=status.HTTP_404_NOT_FOUND
        # return {'detail': f'Blog with the id {id} is not available!'}
        
    return blog

@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_blog_by_id(id, request: Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog with the id of {id} not found')
    
    # update individual blog attributes
    blog.update(request)
    
    # if request.title:
    #     blog.title = request.title
    # if request.body:
    #     blog.body = request.body
    
    blog.update(request)
    
    db.commit()
    
    return 'Blog details successfuly updated'
    

@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_blog_by_id(id, request: Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    blog.delete(synchronize_session=False)
    
    db.commit()
    
    return 'Blog post successfully deleted!'
    