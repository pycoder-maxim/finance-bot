from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from Models import *

engine = create_engine("sqlite:///users.db", echo=True)
Base = declarative_base()
Session = sessionmaker(bind= engine)
session = Session()

user1 = User(name="Alice")
user2 = User(name="Bob")
session.add_all([user1, user2])
session.commit()

print("user_id = ", user1.id)

post1 = Post(user_id= user1.id,title="Всем привет! Меня зовут, Алиса!")
post2 = Post(user_id= user1.id,title="Как Ваши дела?")
session.add_all([post1, post2])
session.commit()

users = session.query(User).all()
for u in users:
    print(u)


posts = session.query(Post).all()
for post in posts:
    print(post)

