from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DataBaseModel import db_path

from UserHandler import UserHandler
from CategoryHandler import CategoryHandler
from ReportsHandler import ReportsHandler
from TransactionsHandler import TransactionsHandler
from WalletHandler import WalletHandler
from CurrenciesHandler import CurrenciesHandler, list_of_default_currencies

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DatabaseApi(metaclass=Singleton):
    def __init__(self):
        engine = create_engine(f"sqlite:///{db_path}") #Cоздание двигателя базы данных SQLite для указанной базы данных с помощью функции create_engine из библиотеки SQLAlchemy.
        __sessionMaker__ = sessionmaker()
        __sessionMaker__.configure(bind=engine)
        self.__session__ = __sessionMaker__()
        self.__db_path__ = db_path # путь к базе данных в файловой системе

        self.__user_hanlder__ = UserHandler(self.__session__)
        self.__category_handler = CategoryHandler(self.__session__)
        self.__report_handler = ReportsHandler(self.__session__)
        self.__trans_handler = TransactionsHandler(self.__session__)
        self.__wallet_handler = WalletHandler(self.__session__)

        self.__currencies_handler = CurrenciesHandler(self.__session__)
        self.__add_default_currencies__()



    def wallets(self):
        return self.__wallet_handler

    def transactions(self):
        return self.__trans_handler

    def users(self):
        return self.__user_hanlder__

    def reporst(self):
        return self.__report_handler

    def categories(self):
        return self.__category_handler

    def currencies(self):
        return self.__currencies_handler

    def __add_default_currencies__(self):
        print("salam")
        # map(lambda cur: self.__currencies_handler.__add_currencies__(*cur), list_of_default_currencies)
        for cur in list_of_default_currencies:
            self.__currencies_handler.__add_currencies__(*cur)