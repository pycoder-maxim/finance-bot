from DataBaseModel import Walets, Users
from sqlalchemy.orm import Session

class WalletHandler:
    def __init__(self, session:Session):
        self.__session__ = session

    def create_wallet(self, name:str, currency:str, created_at:str, user_id:int):
        return Walets(name=name, currency=currency, created_at= created_at)

    def get_wallets_by_user_id(self, user_id:int):
        return self.__session__.query(Walets).filter(Walets.user_id == user_id).all()

    def update_wallet(self, telegram_id: int, name: str = None, currency: str = None) -> bool:
        # TODO - доделать правильную логику
        user = self.__session__.query(Users).filter(Users.telegramm_id == telegram_id).first()
        if not user:
            return False  # Пользователь не найден

        wallet = self.__session__.query(Walets).filter(Walets.user_id == user.id).first()
        if not wallet:
            return False  # Кошелек не найден

        if name:
            wallet.name = name
        if currency:
            wallet.currency = currency

        self.__session__.commit()
        return True

    def delete_wallet(self, telegram_id: int, name: str, currency: str) -> bool:
        user = self.__session__.query(Users).filter(Users.telegramm_id == telegram_id).first()
        if not user:
            return False  # Пользователь не найден
        wallet = (
            self.__session__.query(Walets)
            .filter(Walets.user_id == user.id, Walets.name == name, Walets.currency == currency)
            .first()
        )
        if not wallet:
            return False  # Кошелек не найден

        self.__session__.delete(wallet)
        self.__session__.commit()
        return True
