from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, Boolean, DECIMAL, BigInteger,MetaData
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

db_path = 'database/db/finans_bot_db.db'
Base = declarative_base()

#_______________________________________________________________________________________________________________________
class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    telegramm_id = Column(Integer)
    first_name = Column(String)
    last_name = Column(String)
    user_name = Column(String)
    created_at = Column(String)
    categories = relationship("Categories", back_populates="user")
    wallets = relationship("Wallets", back_populates="user")
    reports = relationship("Reports", back_populates="user")
    transactions = relationship("Transactions", back_populates="user")

    def __init__(self,telegramm_id:int,first_name:str,last_name:str,user_name:str,created_at:str):
        self.telegramm_id = telegramm_id
        self.first_name = first_name
        self.last_name = last_name
        self.user_name = user_name
        self.created_at = created_at

    def __repr__(self):
        info: str = f'Telegramm ID: {self.telegramm_id} {self.first_name} {self.last_name} {self.user_name} ,'\
        f'CREATED AT:{self.created_at}'
        return info

#_______________________________________________________________________________________________________________________

class Currencies(Base):
    __tablename__ = "currencies"
    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True)      # "USD", "RUB"
    name = Column(String)                   # "Российский рубль"
    symbol = Column(String)          # "₽", "$"

    def __init__(self,code:str,name:str,symbol:str):
        self.code = code
        self.name = name
        self.symbol = symbol

    def __repr__(self):
        return f"{self.code} ({self.symbol})"
#_______________________________________________________________________________________________________________________

class Categories(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    ctype = Column(String)  # сокрещение от category type
                            # возможные значения - "income" "expense" "savings" "goal"
    created_at = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("Users",back_populates='categories')

    def __init__(self,name:str,ctype:str,created_at:str):
        self.name = name
        self.ctype = ctype
        self.created_at = created_at

    def __repr__(self):
        info:str = f'ИМЯ, КАТЕГОРИЯ:{self.name} {self.ctype} {self.created_at}'
        return info

#_______________________________________________________________________________________________________________________

class Wallets(Base):
    __tablename__ = 'wallets'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    created_at = Column(String)
    value = Column(DECIMAL(32, 2))
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("Users", back_populates='wallets')
    currency_id = Column(Integer, ForeignKey('currencies.id'))
    currency = relationship("Currencies")

    def __init__(self, user_id:int, name:str, currency:Currencies, created_at:str):
        self.name = name
        self.currency = currency
        self.currency_id = currency.id
        self.created_at = created_at
        self.user_id = user_id
        self.value = 0

    def __repr__(self):
        info:str = f'ИМЯ, ВАЛЮТА:{self.name} {self.currency} {self.created_at}'
        return info

#_______________________________________________________________________________________________________________________

class Reports(Base):
    __tablename__ = 'reports'
    id = Column(Integer, primary_key=True)
    name = Column(String)   # если создан по стандартному предложению,
                            # то назвываем также стандартно - week - mounth - year
                            # иначе называем custom
    report_data = Column(String)
    created_at = Column(String)
    begin_date = Column(String) # начинаем с 00:00 - begin_date
    end_date = Column(String) # время окончания отчета - считаем до 23:59
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("Users", back_populates='reports')
    def __init__(self,name:str,report_data:str,created_at:str, begin:str, end:str):
        self.name = name
        self.report_data = report_data
        self.created_at = created_at
        self.begin_date = begin
        self.end_date = end

    def __repr__(self):
        info:str = f'ИМЯ, ОТЧЕТНЫЕ ДАННЫЕ:{self.name} {self.report_data} {self.created_at}'
        return info

#_______________________________________________________________________________________________________________________

class Transactions(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    #report_data = Column(String)
    created_at = Column(String)
    amount = Column(DECIMAL(32, 2))
    #ttype = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    currency_id = Column(Integer, ForeignKey('currencies.id'))
    wallet_id = Column(Integer, ForeignKey('wallets.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))
    user = relationship("Users", back_populates='transactions')
    wallet = relationship("Wallets")
    category = relationship("Categories")
    currency = relationship("Currencies")

    def __init__(self, user_id: int, name: str, report_data: str, created_at: str,
                 amount: float = 0, ttype: str = None, currency_id: int = None,
                 wallet_id: int = None, category_id: int = None):
        self.name = name
        self.report_data = report_data
        self.created_at = created_at
        self.user_id = user_id
        self.amount = amount
        self.ttype = ttype
        self.currency_id = currency_id
        self.wallet_id = wallet_id
        self.category_id = category_id

    def __repr__(self):
        info:str = f'ИМЯ, ТРАНЗАКЦИЯ:{self.name} {self.report_data} {self.created_at}'
        return info

#_______________________________________________________________________________________________________________________

if __name__ == '__main__':
    engine = create_engine(f"sqlite:///db/finans_bot_db.db")
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    # TODO - сделать создание всех видов валют, которыми пальзуется клиент бота
    print("DATABASE CREATED SUCCESSFULLY\n")


    print(__name__)