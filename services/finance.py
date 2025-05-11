from datetime import datetime
from loader import db_api

def add_transaction(user_id: int, amount: float, category: str, ctype: str, comment: str = ""):
    """Создание транзакции через единый метод."""
    db_api.transactions().add_transaction(
        user_id=user_id,
        amount=amount,
        category=category,
        ttype="income"
    )

def get_balance(user_id: int) -> float:
    income = db_api.transactions().sum_by_type(user_id, "income")
    expense = db_api.transactions().sum_by_type(user_id, "expense")
    return income - expense


def add_expence(user_id: int,amount:float, ctype:str, report:str):
    return

