from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DataBaseModel import db_path

from UserHandler import UserHandler
from CategoryHandler import CategoryHandler
from ReportsHandler import ReportsHandler
from TransactionsHandler import TransactionsHandler
from WalletHandler import WalletHandler


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DatabaseApi(metaclass=Singleton):
    def __init__(self):
        engine = create_engine(f"sqlite:///{db_path}")
        __sessionMaker__ = sessionmaker()
        __sessionMaker__.configure(bind=engine)
        self.__session__ = __sessionMaker__()
        self.__db_path__ = db_path

        self.__user_hanlder__ = UserHandler(self.__session__)
        self.__category_handler = CategoryHandler(self.__session__)
        self.__report_handler = ReportsHandler(self.__session__)
        self.__trans_handler = TransactionsHandler(self.__session__)
        self.__wallet_handler = WalletHandler(self.__session__)

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
