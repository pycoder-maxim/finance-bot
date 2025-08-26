from DataBaseModel import Transactions
from sqlalchemy.orm import Session
import decimal

class TransactionsHandler:
    def __init__(self, session:Session):
        self.__session__ = session

    """
    def create_reports(self, name: str, report_data: str, created_at: str, user_id: int) -> Transactions:
        transactions = Transactions(name=name, report_data=report_data, created_at=created_at)
        transactions.user_id = user_id
        self.__session__.add(transactions)
        self.__session__.commit()
        return transactions
    """

    def get_Transactions_by_user_id(self,user_id: int) -> list[Transactions]:
        return self.__session__.query(Transactions).filter(Transactions.user_id == user_id).all()

    def update_transactions(self, transactions_id: int, **kwargs) -> bool:
        transactions = self.__session__.query(Transactions).get(transactions_id)
        if not transactions:
            return False
        for key, value in kwargs.items():
            if hasattr(transactions, key):
                setattr(transactions, key, value)
        self.__session__.commit()
        return True

    def get_by_type_period(self, user_id, transaction_type, start_date, end_date):
        """
        Получение транзакций по типу за период
        """
        # Преобразуем даты из строк в объекты datetime для сравнения
        from datetime import datetime
        start_dt = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")

        # Фильтруем по пользователю и дате
        transactions = self.__session__.query(Transactions).filter(
            Transactions.user_id == user_id,
            Transactions.created_at.between(start_dt, end_dt)
        ).all()

        # Дополнительная фильтрация по типу транзакции
        if transaction_type == "income":
            return [tr for tr in transactions if tr.amount > 0]
        elif transaction_type == "expense":
            return [tr for tr in transactions if tr.amount < 0]
        else:
            return transactions


    def delete_transactions(self, transactions_id: int) -> bool:
        transaction = self.__session__.query(Transactions).get(transactions_id)
        if not transaction:
            return False
        self.__session__.delete(transaction)
        self.__session__.commit()
        return True

    def add_transaction(self, user_id:int, name: str, report_data: str,created_at: str, amount:float,currency_id: int,wallet_id: int, category_id: int) -> Transactions:
        try:
            transactions = Transactions(user_id, name, report_data, created_at, amount, currency_id, wallet_id ,category_id)
            print(transactions)
            self.__session__.add(transactions)
            self.__session__.commit()
        except Exception as e:
            print(e)
        return transactions