from fastapi import FastAPI, HTTPException, Depends, Query
from database import get_db
from sqlalchemy.orm import Session
import models as m
from typing import List
import pyd
from auth import auth_handler
import bcrypt


app = FastAPI()

@app.post("/api/register", response_model=pyd.SchemeUser)
def register_user(user:pyd.CreateUser, db:Session=Depends(get_db)):
    user_check = db.query(m.User).filter(
        m.User.name == user.name
    ).first()
    if user_check:
        raise HTTPException(404, "Имя пользователя занято!")
    user_db = m.User()

    user_db.name = user.name
    user_db.email = user.email
    user_db.password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())
    user_db.role_id = user.role_id

    db.add(user_db)
    db.commit()

    return user_db

@app.post("/api/login")
def login_user(user:pyd.LoginUser, db:Session=Depends(get_db)):
    user_db = db.query(m.User).filter(
        m.User.name == user.name
    ).first()
    if not user_db:
        raise HTTPException(404, "Пользователь не найден!")
    if auth_handler.verify_password(user.password, user_db.password):
        return {"token": auth_handler.encode_token(user_db.id, user_db.role_id)}
    raise HTTPException(400, "Доступ запрещён!")


@app.patch("/api/post/{id}/like")
def like_state(id:int, db:Session=Depends(get_db), access:m.User=Depends(auth_handler.auth_wrapper)):
    state = db.query(m.State).filter(
        m.State.id == id
    ).first()
    if not state:
        raise HTTPException(404, "Такой статьи не существует!")
    user_db = db.query(m.User).filter(
        m.User.id == access["user_id"]
    ).first()
    if user_db in state.likes:
        raise HTTPException(400, "Вы уже ставили лайк этой статье!")
    state.likes.append(user_db)
    db.add(state)
    db.commit()

    return {"details": "Лайк оставлен!"}


@app.patch("/api/post/{id}/unlike")
def unlike_state(id:int, db:Session=Depends(get_db), access:m.User=Depends(auth_handler.auth_wrapper)):
    state = db.query(m.State).filter(
        m.State.id == id
    ).first()
    if not state:
        raise HTTPException(404, "Такой статьи не существует!")
    user_db = db.query(m.User).filter(
        m.User.id == access["user_id"]
    ).first()
    if user_db not in state.likes:
        raise HTTPException(400, "Вы не оставляли лайк этой статье!")
    state.likes.remove(user_db)
    db.add(state)
    db.commit()
    
    return {"details": "Лайк убран!"}


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
def create_state(state:pyd.CreateState, db:Session=Depends(get_db), access:m.User=Depends(auth_handler.author_wrapper)):
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
def edit_state(id:int, state:pyd.UpdateState, db:Session=Depends(get_db), access:m.User=Depends(auth_handler.author_wrapper)):
    state_db = db.query(m.State).filter(
        m.State.id == id
    ).first()
    if not state_db:
        raise HTTPException(404, "Такой статьи не существует!")
    
    if state.author_id != access["user_id"]:
        if access["role_id"] != 3:
            raise HTTPException(403, "Вы не можете редактировать чужую статью!")

    state_db.title = state.title
    state_db.content = state.content
    state_db.date_publication = state.date_publication
    state_db.status_id = state.status_id
    state_db.author_id = state.author_id
    state_db.category_id = state.category_id

    if access["role_id"] == 3:
        state_db.likes = []
        for like_id in state.likes_id:
            user_db = db.query(m.User).filter(m.User.id == like_id).first()
            if user_db:
                state_db.likes.append(user_db)
            else:
                raise HTTPException(status_code=404, detail=f"Пользователь с id:{like_id} не найден!")

    db.add(state_db)
    db.commit()
    return state_db

@app.delete("/api/post/{id}")
def delete_state(id:int, db:Session=Depends(get_db), access:m.User=Depends(auth_handler.author_wrapper)):
    state_db = db.query(m.State).filter(
        m.State.id == id
    ).first()
    if not state_db:
        raise HTTPException(404, "Такой статьи не существует!")
    
    if state_db.author_id != access["user_id"]:
        if access["role_id"] != 3:
            raise HTTPException(403, "Вы не можете удалить чужую статью!")

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
def create_comment(comment:pyd.CreateComment, db:Session=Depends(get_db), access:m.User=Depends(auth_handler.auth_wrapper)):
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
def edit_comment(id:int, comment:pyd.CreateComment, db:Session=Depends(get_db), access:m.User=Depends(auth_handler.auth_wrapper)):
    check_state = db.query(m.State).filter(
        m.State.id == comment.state_id
    ).first()
    if not check_state:
        raise HTTPException(404, "Такой статьи не существет!")
    
    if comment.user_id != access["user_id"]:
        if access["role_id"] != 3:
            raise HTTPException(403, "Вы не можете редактировать чужой комментарий!")
    
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
def delete_comment(id:int, db:Session=Depends(get_db), access:m.User=Depends(get_db)):
    comment_db = db.query(m.Comment).filter(
        m.Comment.id == id
    ).first()
    if not comment_db:
        raise HTTPException(404, "Такого комментария не существует!")
    
    if comment_db.user_id != access["user_id"]:
        if access["role_id"] != 3:
            raise HTTPException(403, "Вы не можете редактировать чужой комментарий!")
    
    db.delete(comment_db)
    db.commit()

    return {"details": "Комментарий удалён!"}

@app.get("/api/categories", response_model=List[pyd.BaseCategory])
def get_categories(db:Session=Depends(get_db)):
    categories = db.query(m.Category).all()
    return categories

@app.get("/api/category/{id}", response_model=pyd.BaseCategory)
def get_category(id:int, db:Session=Depends(get_db)):
    category = db.query(m.Category).filter(
        m.Category.id == id
    ).first()
    if not category:
        raise HTTPException(404, "Такой категории не существует!")
    return category

@app.post("/api/category/{name}", response_model=pyd.BaseCategory)
def create_category(name:str, db:Session=Depends(get_db), access:m.User=Depends(auth_handler.moderator_wrapper)):
    check_category = db.query(m.Category).filter(
        m.Category.name == name
    ).first()
    if check_category:
        raise HTTPException(400, "Такая категория уже существует!")
    category_db = m.Category()
    category_db.name = name

    db.add(category_db)
    db.commit()

    return category_db

@app.put("/api/category/{id}/{name}", response_model=pyd.BaseCategory)
def edit_category(id:int, name:str, db:Session=Depends(get_db), access:m.User=Depends(auth_handler.moderator_wrapper)):
    check_category = db.query(m.Category).filter(
        m.Category.name == name
    ).first()
    if check_category:
        raise HTTPException(400, "Такая категория уже существует!")
    
    category_db = db.query(m.Category).filter(
        m.Category.id == id
    ).first()
    if not category_db:
        raise HTTPException(400, "Такой категории не существует!")

    category_db.name = name

    db.add(category_db)
    db.commit()

    return category_db

@app.delete("/api/category/{id}")
def delete_category(id:int, db:Session=Depends(get_db), access:m.User=Depends(auth_handler.moderator_wrapper)):
    category_db = db.query(m.Category).filter(
        m.Category.id == id
    ).first()
    if not category_db:
        raise HTTPException(400, "Такой категории не существует!")

    db.delete(category_db)
    db.commit()

    return {"detail": "Категория удалена!"}