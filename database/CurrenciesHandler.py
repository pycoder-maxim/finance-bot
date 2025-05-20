from DataBaseModel import Currencies
from sqlalchemy.orm import Session


class CurrenciesHandler:
    def __init__(self, session:Session):
        self.__session__ = session

    def get_Currencies_by_user_id(self,user_id: int) -> list[Currencies]:
        return self.__session__.query(Currencies).filter(Currencies.user_id == user_id).all()

    def add_currencies(self,  code: str, name:str, symbol:str) -> Currencies:
        currencies = Currencies( code, name, symbol)

        self.__session__.add(currencies)
        self.__session__.commit()
        return currencies

    def update_currencies(self,currencies_id: int, **kwargs) -> bool:
        currencies = self.__session__.query(Currencies).get(currencies_id)
        if not currencies:
            return False
        for key, value in kwargs.items():
            if hasattr(currencies, key):
                setattr(currencies, key, value)
        self.__session__.commit()
        return True

    def delete_currencies(self, currencies_id: int) -> bool:
        currencies = self.__session__.query(Currencies).get(currencies_id)
        if not currencies:
            return False
        self.__session__.delete(currencies)
        self.__session__.commit()
        return True

    def get_curreny_by_code(self, code:str):
        if code == "USD":
            return self.__session__.query(Currencies).filter(Currencies.id == Currencies.id).all()
