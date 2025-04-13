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

users = session.query(User).all()
for u in users:
    print(u)