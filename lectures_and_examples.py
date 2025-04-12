# ORM (Object-Relational Mapping)
"""
ORM
project/
├── main.py            # точка входа
├── models.py          # модели таблиц
└── database.py        # engine + Session + Base
"""

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:////users.db", echo=True)
Base = declarative_base()
Session = sessionmaker(bind= engine)
session = Session()



