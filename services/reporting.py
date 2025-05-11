from datetime import datetime, timedelta
from collections import defaultdict
from loader import db_api

def get_recent_transactions(user_id: int, limit: int = 10):
    """
    Возвращает последние N транзакций пользователя.
    """
    return db_api.transactions().get_last(user_id, limit)

def get_summary_by_category(user_id: int, ttype: str, days: int = 30):
    """
    Возвращает сумму по категориям за последние N дней.
    """
    since = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d %H:%M:%S")
    transactions = db_api.transactions().get_by_type_since(user_id, ttype, since)

    summary = defaultdict(float)
    for tr in transactions:
        summary[tr.category] += tr.amount
    return dict(summary)

def build_text_report(user_id: int, days: int = 30) -> str:
    """
    Формирует текстовый отчёт по доходам и расходам.
    """
    income_summary = get_summary_by_category(user_id, "income", days)
    expense_summary = get_summary_by_category(user_id, "expense", days)

    text = f"📊 Отчёт за последние {days} дней\n\n"

    text += "➕ Доходы:\n"
    if income_summary:
        for cat, amount in income_summary.items():
            text += f"  • {cat}: {amount:.2f} руб\n"
    else:
        text += "  (нет доходов)\n"

    text += "\n➖ Расходы:\n"
    if expense_summary:
        for cat, amount in expense_summary.items():
            text += f"  • {cat}: {amount:.2f} руб\n"
    else:
        text += "  (нет расходов)\n"

    total_income = sum(income_summary.values())
    total_expense = sum(expense_summary.values())
    balance = total_income - total_expense

    text += f"\n💼 Баланс: {balance:.2f} руб"
    return text
