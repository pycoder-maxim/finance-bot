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
post1 = Post(user_id=user.id, title="My first post")

users = session.query(User).all()
for u in users:
    print(u)


post = session.query(Post).first()
print(post.user.name)

user = session.query(User).first()
for post in user.posts:
    print(post.title)

