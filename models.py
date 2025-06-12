from sqlalchemy import Column, Integer, String, Float, Text, Date, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    
class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(65), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"))
    created_at = Column(DateTime(), server_default=func.now())
    
    role = relationship("Role", backref="users")
    
class Status(Base):
    __tablename__ = "statuses"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name =  Column(String(255))
    
class State(Base):
    __tablename__ = "states"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    content = Column(String)
    date_publication = Column(DateTime())
    status_id =  Column(Integer, ForeignKey("statuses.id"))
    likes_amount = Column(Integer, default=0)
    author_id = Column(Integer, ForeignKey("users.id"))
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

    status = relationship("Status", backref="states")
    autor = relationship("User", backref="states")
    category = relationship("Category", backref="states")
    likes = relationship("User", secondary='states_likes')


class StateLike(Base):
    __tablename__="states_likes"
    id=Column(Integer, primary_key=True, autoincrement=True)
    state_id=Column(Integer, ForeignKey('states.id'))
    user_id=Column(Integer, ForeignKey('users.id'))

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String)
    date = Column(DateTime())
    state_id = Column(Integer, ForeignKey("states.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    
    state = relationship("State", backref="commments")
    user = relationship("User", backref="comments")
    