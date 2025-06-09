from pydantic import BaseModel, Field, EmailStr
from datetime import datetime, date
from typing import List

class BaseCategory(BaseModel):
    id: int = Field(example=1)
    name: str = Field(example="Рецепты")
    
class BaseRole(BaseModel):
    id: int = Field(example=1)
    name: str = Field(example="Автор")
    
class BaseUser(BaseModel):
    id: int = Field(example=1)
    name: str = Field(example="Mari")
    email: EmailStr = Field(example="mari@mail.ru")
    
class BaseStatus(BaseModel):
    id: int = Field(example=1)
    name: str = Field(example="Опубликовано")
    
class BaseState(BaseModel):
    id: int = Field(example=1)
    title: str = Field(example="5 способов приготовления картофеля")
    content: str = Field(example="В этой статье мы рассмотрим 5 способо вкусного приготовления картофеля.")
    date_publication: datetime = Field(example="2025-06-01-20:52:00")
    # likes_amount: int = Field(ge=0, example="13")

    
class BaseComment(BaseModel):
    id: int = Field(example=1)
    text: str = Field(example="Спасибо, очень вкусно")
    date: datetime = Field(example="2025-06-01-21:02:00")
    