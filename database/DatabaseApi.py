from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from UserHandler import UserHandler
#from TransactionsHandler import TransactionHandler
#from LinkHandler import LinkHandler
#from CommissionHandler import CommissionHandler
#from DatabaseModel import db_path
#from WalletHandler import WalletHandler


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DatabaseApi(metaclass=Singleton):
    def __init__(self):
        engine = create_engine(f"postgresql+psycopg2://{db_path}")
        __sessionMaker__ = sessionmaker()
        __sessionMaker__.configure(bind=engine)
        self.__session__ = __sessionMaker__()
        #self.__db_path__ = db_path
        #self.__userHandle__ = UserHandler(self.__session__)

        #self.__transactionHandle__ = TransactionHandler(self.__session__)
        #self.__walletHandle__ = WalletHandler(self.__session__, self.__userHandle__)

        #self.__linkHandle__ = LinkHandler(self.__session__)
        #self.__commissionHandle__ = CommissionHandler(self.__session__)

    def wallets(self):
        return self.__walletHandle__

    def transactions(self):
        return self.__transactionHandle__

    def users(self):
        return self.__userHandle__

    def links(self):
        return self.__linkHandle__

    def commissions(self):
        return self.__commissionHandle__
