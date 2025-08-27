from DataBaseModel import Transactions
from sqlalchemy.orm import Session
import decimal

class TransactionsHandler:
    def __init__(self, session:Session):
        self.__session__ = session



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

        print(f"🔄 DEBUG: Filtering transactions for user {user_id}")
        print(f"🔄 DEBUG: Date range: {start_dt} to {end_dt}")

        # Фильтруем по пользователю и дате
        transactions = self.__session__.query(Transactions).filter(
            Transactions.user_id == user_id,
            Transactions.created_at.between(start_dt, end_dt)
        ).all()

        print(f"🔄 DEBUG: Found {len(transactions)} transactions in date range")

        # Дополнительная фильтрация по типу транзакции
        if transaction_type == "income":
            result = [tr for tr in transactions if tr.amount > 0]
            print(f"🔄 DEBUG: Filtered {len(result)} income transactions")
            return result
        elif transaction_type == "expense":
            result = [tr for tr in transactions if tr.amount < 0]
            print(f"🔄 DEBUG: Filtered {len(result)} expense transactions")
            return result
        else:
            print(f"🔄 DEBUG: Returning all {len(transactions)} transactions")
            return transactions

    def get_transactions_by_user_and_period(self, user_id, start_date, end_date):
        """Получить транзакции пользователя за указанный период"""
        return self.__session__.query(Transactions).filter(
            Transactions.user_id == user_id,
            Transactions.created_at >= start_date,
            Transactions.created_at <= end_date
        ).all()



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