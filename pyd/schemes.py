from .basemodels import *
from typing import List

class SchemeState(BaseState):
    likes: List[BaseUser]
    status: BaseStatus
    autor: BaseUser
    category: None|BaseCategory

class SchemeComment(BaseComment):
    state: BaseState
    user: BaseUser

class SchemeUser(BaseUser):
    role: BaseRole
