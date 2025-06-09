from .basemodels import *
from typing import List

class SchemeState(BaseState):
    likes: List[BaseUser]
    status: BaseStatus
    autor: BaseUser
    category: BaseCategory
