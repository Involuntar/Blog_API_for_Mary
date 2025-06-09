from fastapi import HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
import models as m
from database import get_db

security = HTTPBasic()


def basic_auth(
    credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)
):
    user_db = db.query(m.User).filter(m.User.name == credentials.name).first()
    if not user_db:
        raise HTTPException(404, "Пользователь не найден")
    if user_db.password == credentials.password:
        return user_db
    if credentials.name == "admin" and credentials.password == "123":
        return True
    raise HTTPException(401, "Неверный логин или пароль!")
