from DataBaseModel import Wallets, Users
from sqlalchemy.orm import Session
from DataBaseModel import Currencies
class WalletHandler:
    def __init__(self, session:Session):
        self.__session__ = session

    def create_wallet(self, user_id: int,   name:str, currency:Currencies, created_at:str, ):
        wallet = Wallets(user_id=user_id,   name=name, currency=currency,  created_at= created_at)
        self.__session__.add(wallet)
        self.__session__.commit()
        return wallet

    def get_wallets_by_user_id(self, user_id:int):
        return self.__session__.query(Wallets).filter(Wallets.user_id == user_id).all()

    def get_wallets_by_id(self, id:int):
        return self.__session__.query(Wallets).filter(Wallets.id == id).first()

    def get_wallets_by_user_id_and_cur_id(self, user_id:int, cur_id:int) -> Wallets:
        return self.__session__.query(Wallets).filter(Wallets.user_id == user_id, Wallets.currency_id == cur_id).all()

    def update_wallet(self, telegram_id: int,  **kwargs) -> bool:
        user = self.__session__.query(Wallets).get(telegram_id)
        if not user:
            return False
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
        self.__session__.commit()
        return True


    def delete_wallet(self, wall_id : int) -> bool:
        wallet = (
            self.__session__.query(Wallets)
            .filter(Wallets.id == wall_id)
            .first()
        )
        if not wallet:
            return False  # Кошелек не найден

        self.__session__.delete(wallet)
        self.__session__.commit()
        return True
