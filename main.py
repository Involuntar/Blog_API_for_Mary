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
def post_state(state:pyd.CreateState, db:Session=Depends(get_db)):
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
