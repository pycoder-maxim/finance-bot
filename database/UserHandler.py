from DataBaseModel import Users, Walets
from sqlalchemy.orm import Session
from datetime import datetime, date, time, timedelta

class UserHandler:
    def __init__(self, session: Session):
        self.__session__ = session

    def get_by_id(self, telegram_id: int) -> Users:
        return self.__session__.query(Users).filter(Users.telegramm_id == telegram_id).first()

    def add_user(self, telegram_id: int, first_name: str, last_name: str, user_name: str, created_at: str) -> bool:
        if self.get_by_id(telegram_id):
            return False  # User already exists

        user = Users(
            telegramm_id=telegram_id,
            first_name=first_name,
            last_name=last_name,
            user_name=user_name,
            created_at=created_at
        )

        self.__session__.add(user)
        self.__session__.commit()

        wallet_rub_cash = Walets(user.telegramm_id, name="Наличные рубли", currency="RUB", created_at= created_at)
        wallet_usd_cash = Walets(user.telegramm_id, name="Наличные доллары", currency="USD", created_at= created_at)
        wallet_rub_card_sber = Walets(user.telegramm_id, name = "Карта Сбер", currency="RUB", created_at= created_at)

        #self.__session__.add(user)
        #self.__session__.commit()

        #wallet_rub_cash.user_id = user
        #wallet_usd_cash.user_id = user
        #wallet_rub_card_sber.user_id = user

        #self.__session__.add_all([wallet_rub_cash, wallet_usd_cash, wallet_rub_card_sber])
        self.__session__.add(wallet_rub_cash)
        self.__session__.add(wallet_usd_cash)
        self.__session__.add(wallet_rub_card_sber)

        self.__session__.commit()

        return True

    def delete_user(self, telegram_id: int) -> bool:
        user = self.get_by_id(telegram_id)
        if not user:
            return False
        self.__session__.delete(user)
        self.__session__.commit()
        return True

    def update_user(self, telegram_id: int, **kwargs) -> bool:
        user = self.get_by_id(telegram_id)
        if not user:
            return False
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
        self.__session__.commit()
        return True

    def get_all_users(self) -> list[Users]:
        return self.__session__.query(Users).all()
