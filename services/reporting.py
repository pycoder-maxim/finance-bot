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

TTYPE_INCOME = 'income'
TTYPE_EXPENCE = 'expense'

def _norm_date(dt: str | datetime) -> str:
    if isinstance(dt, datetime):
        return dt.strftime("%y-%m-%d %H:%M:%S")
    return dt


def category_totals(
        user_id:int,
        date_frome: str | datetime,
        date_to : str | datetime,
        ttype: Optional[str] = None,
        wallet_ids: Optional[List[int]] = None,
        currency_id: Optional[int] = None,
        top_n: Optional[int] = None
) -> List[Dict]:
    df = _norm_date(date_frome)
    dt = _norm_date(date_to)

    # Условия запроса для ОРМ
    conditiones = [
        Transactions.user_id == user_id,
        Transactions.created_at >= df,
        Transactions.created_at <= dt,
        Transactions.category_id.isnot(None)
    ]
    if ttype:
        conditiones.append(Transactions.name == ttype)
    if wallet_ids:
        conditiones.append(Transactions.wallet_id.in_(wallet_ids))
    if currency_id:
        conditiones.append(Transactions.currency_id == currency_id)

    stmt = (
        select(
            Categories.id.label("category_id"),
            Categories.name.label("category"),
            func.coalesce(func.sum(Transactions.amount), 0).label("total")
        )
        .join(Categories, Categories.id == Transactions.category_id)
        .where(and_(*conditiones))
        .group_by(Categories.id, Categories.name)
        .order_by(func.sum(Transactions.amount).desc())
    )

    if top_n:
        stmt = stmt.limit(top_n)

    rows = db_api.__session__.execute(stmt).all()
    return [{"category_id": r.category_id, "category": r.category, "total": float(r.total)} for r in rows]


def category_breakdown(
        user_id : int,
        category_id : int,
        date_from : str | datetime,
        date_to : str | datetime,
        ttype : Optional[str] = None,
        wallet_ids : Optional[List[int]] = None,
        currency_id : Optional[int] = None,
        limit: int = 20,
        offset: int = 0
) -> List[Dict]:
    """Детализация по конкретной категории: список транзакций (для раскрытия «вглубь»)."""

    df = _norm_date(date_from)
    dt = _norm_date(date_to)

    conditions = [
        Transactions.user_id == user_id,
        Transactions.created_at >= df,
        Transactions.created_at <= dt,
        Transactions.category_id == category_id
    ]
    if ttype:
        conditions.append(Transactions.name == ttype)
    if wallet_ids:
        conditions.append(Transactions.wallet_id.in_(wallet_ids))
    if currency_id:
        conditions.append(Transactions.currency_id == currency_id)

    stmt = (
        select(
            Transactions.id,
            Transactions.created_at,
            Transactions.amount,
            Transactions.report_data,
            Wallets.name.label("wallet"),
            Currencies.code.label("currency")
        )
        .join(Wallets, Wallets.id == Transactions.wallet_id, isouter=True)
        .join(Currencies, Currencies.id == Transactions.currency_id, isouter=True)
        .where(and_(*conditions))
        .order_by(Transactions.created_at.desc())
        .limit(limit)
        .offset(offset)
    )

    rows = db_api.__session__.execute(stmt).all()
    result = []
    for r in rows:
        result.append({
            "id": r.id,
            "created_at": r.created_at,
            "amount": float(r.amount),
            "currency": r.currency,
            "wallet": r.wallet,
            "comment": r.report_data
        })
    return result












