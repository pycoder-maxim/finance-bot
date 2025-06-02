from DataBaseModel import Users, Wallets, Currencies,Categories
from sqlalchemy.orm import Session
from database import CategoryHandler

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

        #доходы
        for income in CategoryHandler.categories_of_icomes:
            category = Categories(name=income, ctype="income", created_at=created_at)
            category.user_id = telegram_id
            self.__session__.add(category)

        # расходы
        for expense in CategoryHandler.categories_of_expenses:
            category = Categories(name=expense, ctype="expense", created_at=created_at)
            category.user_id = telegram_id
            self.__session__.add(category)

        # сбережения
        for savings in CategoryHandler.categories_of_savings:
            category = Categories(name=savings, ctype="savings", created_at=created_at)
            category.user_id = telegram_id
            self.__session__.add(category)

        # цели
        for goals in CategoryHandler.categories_of_goals:
            category = Categories(name=goals, ctype="goals", created_at=created_at)
            category.user_id = telegram_id
            self.__session__.add(category)

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
