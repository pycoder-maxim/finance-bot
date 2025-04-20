from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, Boolean, DECIMAL, BigInteger
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

db_path = 'database/db/finans_bot_db.db'
Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    telegramm_id = Column(Integer)
    first_name = Column(String)
    last_name = Column(String)
    user_name = Column(String)
    created_at = Column(String)
    categories = relationship("Categories", back_populates="users")

    def __init__(self,telegramm_id:int,first_name:str,last_name:str,user_name:str,created_at:str):
        self.telegramm_id = telegramm_id
        self.first_name = first_name[0]
        self.last_name = last_name[1]
        self.user_name = user_name[2]
        self.created_at = created_at

    def __repr__(self):
        info: str = f'Telegramm ID: {self.telegramm_id} {self.first_name} {self.last_name} {self.user_name} ,'\
        f'CREATED AT:{self.created_at}'
        return info


class Categories(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    ctype = Column(String) # сокрещение от category type
    # возможные значения - "income" "expense" "savings" "goal"

    created_at = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    users = relationship("Users",back_populates='categories')

    def __init__(self,name:str,ctype:str,created_at:str):
        self.name = name
        self.ctype = ctype
        self.created_at = created_at

    def __repr__(self):
        info:str = f'ИМЯ, КАТЕГОРИЯ:{self.name} {self.ctype} {self.created_at}'
        return info


class Walets(Base):
    __tablename__ = 'walets'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    currency = Column(String)
    created_at = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    walets = relationship("Users", back_populates='walets')
    def __init__(self, user_id:int, name:str,currency:str,created_at:str):
        self.name = name
        self.currency = currency
        self.created_at = created_at
        self.user_id = user_id

    def __repr__(self):
        info:str = f'ИМЯ, ВАЛЮТА:{self.name} {self.currency} {self.created_at}'
        return info
    #

class Reports(Base):
    __tablename__ = 'reports'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    report_data = Column(String)
    created_at = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    walets = relationship("Users", back_populates='reports')
    def __init__(self,name:str,report_data:str,created_at:str):
        self.name = name
        self.report_data = report_data
        self.created_at = created_at


    def __repr__(self):
        info:str = f'ИМЯ, ПОВТОРНО ОБРАБОТАННЫЕ ДАННЫЕ:{self.name} {self.currency} {self.created_at}'
        return info



class Transactions(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    report_data = Column(String)
    created_at = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    walets = relationship("Users", back_populates='transactions')
    def __init__(self,name:str,report_data:str,created_at:str):
        self.name = name
        self.report_data = report_data
        self.created_at = created_at


    def __repr__(self):
        info:str = f'ИМЯ, ПОВТОРНО ОБРАБОТАННЫЕ ДАННЫЕ:{self.name} {self.currency} {self.created_at}'
        return info


if __name__ == '__main__':
    engine = create_engine(f"sqlite:///{db_path}")
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    print("DATABASE CREATED SUCCESSFULLY\n")
    print(__name__)