from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.dialects.oracle.dictionary import all_users
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from Models import *

engine = create_engine("sqlite:///users.db", echo=True)
Base = declarative_base()
Session = sessionmaker(bind= engine)
session = Session()




cat = session.query(Comments).filter_by(name="Зарплата").first()
cat.name = "Зарплата"
session.commit()

