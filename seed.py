from sqlalchemy.orm import Session
from database import engine
import models as m
from datetime import datetime as dt

m.Base.metadata.drop_all(bind=engine)
m.Base.metadata.create_all(bind=engine)

with Session(bind=engine) as session:
    state1 = m.State(
        title="Как засолить огурчики",
        content="Статья про огурчики, вкусные огурчики",
        date_publication=dt.strptime("2019-01-01T08:00:00Z", "%Y-%m-%dT%H:%M:%SZ").date(),
        category_id="1",
        status_id="1",
        author_id="1"
    )
    session.add(state1)
    state2 = m.State(
        title="Never ending story",
        content="Cats for cats",
        date_publication=dt.strptime("2020-01-01T08:00:00Z", "%Y-%m-%dT%H:%M:%SZ").date(),
        category_id="1",
        status_id="1",
        author_id="1"
    )
    session.add(state2)
    
    comment1 = m.Comment(
        text="cool",
        date=dt.strptime("2019-02-01T08:20:00Z", "%Y-%m-%dT%H:%M:%SZ").date(),
        state_id="1",
        user_id="1"
    )
    session.add(comment1)
    comment2 = m.Comment(
        text="so pity",
        date=dt.strptime("2020-03-01T08:20:00Z", "%Y-%m-%dT%H:%M:%SZ").date(),
        state_id="1",
        user_id="1"
    )
    session.add(comment2)
    
    user1 = m.User(
        name="Ami",
        password="666666",
        email="mari@mail.ru"
    )
    session.add(user1)
    
    role1 = m.Role(name="читатель")
    session.add(role1)
    
    category1 = m.Category(name="Еда")
    session.add(category1)
    category2 = m.Category(name="Sadness")
    session.add(category2)
    
    status1 = m.Status(name="Черновик")
    session.add(status1)
    status2 = m.Status(name="published")
    session.add(status2)

    l1 = m.StateLike(user_id=1, state_id=1)
    session.add(l1)
    
    session.commit()