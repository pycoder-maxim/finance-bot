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


def generate_report(user_id: int, start_date: datetime, end_date: datetime, period_text: str) -> str:
    """
    Генерирует финансовый отчет для пользователя за указанный период
    """
    try:
        # Получаем данные из базы
        transactions = db_api.transactions().get_transactions_by_user_and_period(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date
        )

        # Получаем информацию о кошельках
        wallets = db_api.wallets().get_wallets_by_user_id(user_id=user_id)

        # Рассчитываем общие суммы
        total_income = 0
        total_expense = 0

        # Группируем по категориям
        income_by_category = {}
        expense_by_category = {}

        for transaction in transactions:
            if transaction.type == 'income':
                total_income += transaction.amount
                if transaction.category_name not in income_by_category:
                    income_by_category[transaction.category_name] = 0
                income_by_category[transaction.category_name] += transaction.amount
            elif transaction.type == 'expense':
                total_expense += transaction.amount
                if transaction.category_name not in expense_by_category:
                    expense_by_category[transaction.category_name] = 0
                expense_by_category[transaction.category_name] += transaction.amount

        # Формируем текст отчета
        report_text = f"<b>📊 Отчет за {period_text}</b>\n"
        report_text += f"<b>Период:</b> {start_date.strftime('%d.%m.%Y')} - {end_date.strftime('%d.%m.%Y')}\n\n"

        report_text += f"<b>💰 Доходы:</b> {total_income:.2f} руб.\n"
        if income_by_category:
            report_text += "<b>По категориям:</b>\n"
            for category, amount in income_by_category.items():
                report_text += f"  • {category}: {amount:.2f} руб.\n"
        report_text += "\n"

        report_text += f"<b>💸 Расходы:</b> {total_expense:.2f} руб.\n"
        if expense_by_category:
            report_text += "<b>По категориям:</b>\n"
            for category, amount in expense_by_category.items():
                report_text += f"  • {category}: {amount:.2f} руб.\n"
        report_text += "\n"

        report_text += f"<b>📈 Баланс:</b> {total_income - total_expense:.2f} руб.\n\n"

        # Добавляем информацию о кошельках
        report_text += "<b>💼 Состояние кошельков:</b>\n"
        for wallet in wallets:
            report_text += f"  • {wallet.name}: {wallet.value:.2f} руб.\n"

        return report_text

    except Exception as e:
        logger.error(f"Error generating report: {e}")
        return "❌ Произошла ошибка при формировании отчета"



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


from sqlalchemy import func, select, and_
from sqlalchemy.orm import Session, joinedload
from datetime import datetime
from typing import Optional, List, Dict, Tuple

from database.DataBaseModel import Transactions, Categories, Wallets, Currencies
from loader import db_api
