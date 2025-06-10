from fastapi import FastAPI, HTTPException, Depends, UploadFile, Query, Form
from database import get_db
from sqlalchemy.orm import Session
import models as m
from typing import List
import pyd
import shutil
from fastapi.staticfiles import StaticFiles
import string
import random
import os
from auth import basic_auth


app = FastAPI()

@app.get("/api/posts", response_model=List[pyd.SchemeState])
def get_all_states(limit:None|int=Query(10,lt=100), page:None|int=Query(1),category:None|int=Query(None),status:None|int=Query(None),db: Session = Depends(get_db)):
    states = db.query(m.State)
    if status:
        states = states.filter(m.State.status_id == status)
    if category:
        states = states.filter(m.State.category_id == category)
    if limit:
        states = states[(page-1)*limit:page*limit]
        if not states:
            raise HTTPException(404, "Статьи не найдены!")
        return states
    get_states = states.all()
    if not get_states:
        raise HTTPException(404, "Статьи не найдены!")
    return get_states


@app.get("/api/post/{id}", response_model=pyd.SchemeState)
def get_state(id:int, db:Session=Depends(get_db)):
    state = db.query(m.State).filter(
        m.State.id == id
    ).first()
    if not state:
        raise HTTPException(404, "Статья не найдена!")
    return state

@app.post("/api/posts", response_model=pyd.SchemeState)
def create_state(state:pyd.CreateState, db:Session=Depends(get_db)):
    check_user = db.query(m.User).filter(
        m.User.id == state.author_id
    ).first()
    if not check_user:
        raise HTTPException(404, "Такого пользователя не существет!")

    state_db = m.State()

    state_db.title = state.title
    state_db.content = state.content
    state_db.date_publication = state.date_publication
    state_db.status_id = state.status_id
    state_db.author_id = state.author_id
    state_db.category_id = state.category_id

    db.add(state_db)
    db.commit()
    return state_db

@app.put("/api/post/{id}", response_model=pyd.SchemeState)
def edit_state(id:int, state:pyd.CreateState, db:Session=Depends(get_db)):
    state_db = db.query(m.State).filter(
        m.State.id == id
    ).first()
    if not state_db:
        raise HTTPException(404, "Такой статьи не существует!")

    state_db.title = state.title
    state_db.content = state.content
    state_db.date_publication = state.date_publication
    state_db.status_id = state.status_id
    state_db.author_id = state.author_id
    state_db.category_id = state.category_id

    db.add(state_db)
    db.commit()
    return state_db

@app.delete("/api/post/{id}")
def delete_state(id:int, db:Session=Depends(get_db)):
    state_db = db.query(m.State).filter(
        m.State.id == id
    ).first()
    if not state_db:
        raise HTTPException(404, "Такой статьи не существует!")
    db.delete(state_db)
    db.commit()

    return {"details": "Статья удалена"}


@app.get("/api/comments", response_model=List[pyd.SchemeComment])
def get_comments(db:Session=Depends(get_db)):
    comments = db.query(m.Comment).all()
    if not comments:
        raise HTTPException(404, "Комментариев нет!")
    return comments

@app.get("/api/comment/{id}", response_model=pyd.SchemeComment)
def get_comment(id:int, db:Session=Depends(get_db)):
    comment = db.query(m.Comment).filter(
        m.Comment.id == id
    ).first()
    if not comment:
        raise HTTPException(404, "Такого комментария не существует!")
    return comment

@app.post("/api/comment", response_model=pyd.SchemeComment)
def create_comment(comment:pyd.CreateComment, db:Session=Depends(get_db)):
    check_state = db.query(m.State).filter(
        m.State.id == comment.state_id
    ).first()
    if not check_state:
        raise HTTPException(404, "Такой статьи не существет!")
    
    check_user = db.query(m.User).filter(
        m.User.id == comment.user_id
    ).first()
    if not check_user:
        raise HTTPException(404, "Такого пользователя не существет!")
    
    comment_db = m.Comment()

    comment_db.text = comment.text
    comment_db.date = comment.date
    comment_db.state_id = comment.state_id
    comment_db.user_id = comment.user_id

    db.add(comment_db)
    db.commit()

    return comment_db

@app.put("/api/comment/{id}", response_model=pyd.SchemeComment)
def edit_comment(id:int, comment:pyd.CreateComment, db:Session=Depends(get_db)):
    check_state = db.query(m.State).filter(
        m.State.id == comment.state_id
    ).first()
    if not check_state:
        raise HTTPException(404, "Такой статьи не существет!")
    
    check_user = db.query(m.User).filter(
        m.User.id == comment.user_id
    ).first()
    if not check_user:
        raise HTTPException(404, "Такого пользователя не существет!")
    comment_db = db.query(m.Comment).filter(
        m.Comment.id == id
    ).first()
    if not comment_db:
        raise HTTPException(404, "Такого комментария не существует!")
    
    comment_db.text = comment.text
    comment_db.date = comment.date
    comment_db.state_id = comment.state_id
    comment_db.user_id = comment.user_id

    db.add(comment_db)
    db.commit()

    return comment_db


@app.delete("/api/comment/{id}")
def delete_comment(id:int, db:Session=Depends(get_db)):
    comment_db = db.query(m.Comment).filter(
        m.Comment.id == id
    ).first()
    if not comment_db:
        raise HTTPException(404, "Такого комментария не существует!")
    
    db.delete(comment_db)
    db.commit()

    return {"details": "Комментарий удалён!"}

