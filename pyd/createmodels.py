from pydantic import BaseModel, Field, EmailStr
from datetime import datetime, date
from typing import List

class CreateCategory(BaseModel):
    name: str = Field(example="Рецепты")
    
class CreateRole(BaseModel):
    name: str = Field(example="Автор")
    
class CreateUser(BaseModel):
    name: str = Field(example="Mari", min_length=2, max_length=60)
    password: str = Field(min_length=6, max_length=60)
    email: EmailStr = Field(example="mari@mail.ru")
    role_id:int=Field(example=1)
    
class CreateStatus(BaseModel):
    name: str = Field(example="Опубликовано")
    
class CreateState(BaseModel):
    title: str = Field(example="5 способов приготовления картофеля")
    content: str = Field(example="В этой статье мы рассмотрим 5 способо вкусного приготовления картофеля.")
    date_publication: datetime = Field(example="2025-06-01 20:52:00")
    status_id:int=Field(example=1)
    author_id:int=Field(example=1)
    category_id:int=Field(example=1)

class UpdateState(BaseModel):
    title: str = Field(example="5 способов приготовления картофеля")
    content: str = Field(example="В этой статье мы рассмотрим 5 способо вкусного приготовления картофеля.")
    date_publication: datetime = Field(example="2025-06-01 20:52:00")
    # likes_amount: int = Field(ge=0, example="13")
    status_id:int=Field(example=1)
    author_id:int=Field(example=1)
    category_id:int=Field(example=1)
    likes_id:List|None=Field(example=[1, 3])
    
class CreateComment(BaseModel):
    text: str = Field(example="Спасибо, очень вкусно")
    date: datetime = Field(example="2025-06-01 21:02:00")
    state_id: int = Field(example=1)
    user_id: int = Field(example=1)

class LoginUser(BaseModel):
    name:str=Field(example="user", min_length=2, max_length=60)
    password:str=Field(min_length=6, max_length=60)
    