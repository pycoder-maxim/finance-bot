from .DataBaseModel import Wallets, Users
from sqlalchemy.orm import Session
import datetime
from sqlalchemy import func
from .DataBaseModel import Currencies
from .DataBaseModel import Wallets, Users, Currencies
from sqlalchemy.orm import Session
import datetime
from sqlalchemy import func



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

    def update_balance(self, user_id: int, value: float, wall_id: int) -> bool:
        wallet = self.__session__.query(Wallets).filter(Wallets.id == int(wall_id), Wallets.user_id == int(user_id)).first()
        if not wallet:
            print(f"Кошелёк не найден (user_id={user_id}, wallet_id={wall_id})")
            return False
        wallet.value = value
        self.__session__.commit()

    def add_to_balance(self, user_id: int, amount: float, wall_id: int = None) -> bool:
        try:

            wallet = None
            if wall_id:
                wallet = self.__session__.query(Wallets).filter(
                    Wallets.id == wall_id,
                    Wallets.user_id == user_id
                ).first()

            if not wallet:
                default_currency = self.__session__.query(Currencies).first()
                if not default_currency:
                    raise ValueError("Нет доступных валют в системе")

                wallet = self.create_wallet(
                    user_id=user_id,
                    name="Основной",
                    currency=default_currency,
                    created_at=datetime.datetime.now().__str__()
                )
                print(f"✅ Создан новый кошелёк (id={wallet.id}) для user_id={user_id}")

            wallet.value += amount
            self.__session__.commit()
            return True

        except Exception as e:
            print(f"❌ Ошибка в add_to_balance: {str(e)}")
            self.__session__.rollback()
            return False

    def get_total_balance(self, user_id: int) -> float:
        total = (
            self.__session__.query(func.sum(Wallets.value))
            .filter(Wallets.user_id == user_id)
            .scalar()
        )
        return float(total) if total else 0.0






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
