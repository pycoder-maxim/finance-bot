from DataBaseModel import Users, Wallets, Currencies,Categories
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

        list_all_currs = self.__session__.query(Currencies).all()

        list_of_wallets_cash = [Wallets(user.telegramm_id, f"Наличные {cur.name}", cur, created_at) for cur in list_all_currs]
        list_of_wallets_cards = [Wallets(user.telegramm_id, f"Крадитна карта - {cur.name}", cur, created_at) for cur in list_all_currs]

        print(list_of_wallets_cards)
        print(list_of_wallets_cash)

        list_all_cat = self.__session__.query(Categories).all()

        categories_of_expenses = [Categories(user.telegramm_id,"Категории расходов",)]
        categories_of_icomes = [Categories(user.telegramm_id,"Категории доходов",)]







        # wallet_rub_cash = Wallets(user.telegramm_id, name="Наличные рубли", currency="RUB", created_at= created_at)
        # wallet_usd_cash = Wallets(user.telegramm_id, name="Наличные доллары", currency="USD", created_at= created_at)
        # wallet_rub_card_sber = Wallets(user.telegramm_id, name = "Карта Сбер", currency="RUB", created_at= created_at)
        for wal in list_of_wallets_cards + list_of_wallets_cash:
            self.__session__.add(wal, True)
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
