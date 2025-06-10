from sqlalchemy.orm import Session
from database import engine
import models as m
from datetime import datetime as dt
import bcrypt

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
        password=bcrypt.hashpw(b'666666', bcrypt.gensalt()),
        email="mari@mail.ru",
        role_id="2"
    )
    session.add(user1)

    user2 = m.User(
        name="Ivan",
        password=bcrypt.hashpw(b'IvanPassword', bcrypt.gensalt()),
        email="ivan@mail.ru",
        role_id="2"
    )
    session.add(user2)

    user3 = m.User(
        name="Moder",
        password=bcrypt.hashpw(b'roooooot', bcrypt.gensalt()),
        email="moder@mail.ru",
        role_id="3"
    )
    session.add(user3)
    
    role1 = m.Role(name="Читатель")
    session.add(role1)

    role2 = m.Role(name="Автор")
    session.add(role2)

    role3 = m.Role(name="Модератор")
    session.add(role3)
    
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