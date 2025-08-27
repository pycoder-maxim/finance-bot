from database import Currencies,Wallets, Categories
from telebot import types
from telebot.states import State, StatesGroup
from telebot.states.sync.context import StateContext
import datetime
from datetime import timedelta
from database.build.lib.DataBaseModel import Currencies, Categories, Wallets
from handlers.transactions_states import MyStates
from loader import bot, db_api
import keybords
from telebot.types import CallbackQuery
from datetime import datetime, timedelta
import datetime as std_datetime
from telebot.types import CallbackQuery, Message
import logging
logger = logging.getLogger(__name__)


class Balance_and_Reports_States(StatesGroup):
    begin_state = State()
    input_reports_state = State()
    check_ballence_state = State()
    custom_period_state = State()

@bot.callback_query_handler(func=lambda call: True, state=Balance_and_Reports_States.begin_state)
def begin_state(call:CallbackQuery, state: StateContext):
    if call.data == 'show_reports':
        state.set(Balance_and_Reports_States.input_reports_state)
        markup = keybords.reports_time_piriod()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text='Выберите промежуток дохода  📅',
                              reply_markup=markup)

    elif call.data == 'go_to_back_menu':
        state.delete()
        state.set(MyStates.start_choice)
        markup = keybords.transaction_status_changing_categories()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text='Выберете нужную команду',
                              reply_markup=markup)
    elif call.data == 'go_to_back_menu_fin':
        state.delete()
        state.set(MyStates.start_choice)
        markup = keybords.transaction_status_changing_categories()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text='Выберете нужную команду',
                              reply_markup=markup)



        state.delete()

@bot.callback_query_handler(func=lambda call: True, state=Balance_and_Reports_States.input_reports_state)
def input_state(call:CallbackQuery, state: StateContext):

    user_id = call.from_user.id
    start_date = None
    end_date = None
    period_text = None

    if call.data == 'report for the day':
        start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)
        period_text = "день"

    elif call.data == 'report for the week':
        start_date = datetime.now() - timedelta(days=datetime.now().weekday())
        start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = start_date + timedelta(days=6, hours=23, minutes=59, seconds=59)
        period_text = "неделю"

    elif call.data == 'report for the mounth':
        start_date = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        start_date = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        next_month = datetime.now().replace(day=28) + timedelta(days=4)
        end_date = next_month - timedelta(days=next_month.day)
        end_date = end_date.replace(hour=23, minute=59, second=59, microsecond=999999)
        period_text = "месяц"

    elif call.data == 'report for the year':
        start_date = datetime.now().replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        end_date = datetime.now().replace(month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)

    elif call.data == 'custom_period':
        state.set(Balance_and_Reports_States.custom_period_state)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text='Введите период в формате: ДД.ММ.ГГГГ-ДД.ММ.ГГГГ\nНапример: 01.01.2023-31.01.2023')
        return

    elif call.data == 'go_back':
        state.delete()
        state.set(Balance_and_Reports_States.begin_state)
        markup = keybords.reports_and_ballance()
        wallets = db_api.wallets().get_wallets_by_user_id(user_id=call.from_user.id)
        wallet_info = ''
        for wallet in wallets:
            wallet_info += f'{wallet.name}:  {wallet.value} руб.\n'
        bold_title = '<b>➕💼 Сумма ваших кошельков:</b>'
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text=f'{bold_title} : \n\n {wallet_info} ',
                              reply_markup=markup, parse_mode='HTML')
        return
    if start_date and end_date and period_text:
        report_text = generate_report(user_id, start_date, end_date, period_text)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.id,
            text=report_text,
            reply_markup=keybords.back_to_reports_button(),
            parse_mode='HTML'
        )


def generate_report(user_id: int, start_date: datetime, end_date: datetime, period_text: str) -> str:
    """
    Генерирует финансовый отчет для пользователя за указанный период
    """
    try:

        transactions = db_api.transactions().get_transactions_by_user_and_period(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date
        )


        wallets = db_api.wallets().get_wallets_by_user_id(user_id=user_id)


        total_income = 0
        total_expense = 0


        income_by_category = {}
        expense_by_category = {}

        for transaction in transactions:

            if transaction.amount > 0:  # Доход
                total_income += transaction.amount

                category = db_api.categories().get_category_by_id(transaction.category_id)
                category_name = category.name if category else "Без категории"

                if category_name not in income_by_category:
                    income_by_category[category_name] = 0
                income_by_category[category_name] += transaction.amount

            elif transaction.amount < 0:
                total_expense += abs(transaction.amount)

                category = db_api.categories().get_category_by_id(transaction.category_id)
                category_name = category.name if category else "Без категории"

                if category_name not in expense_by_category:
                    expense_by_category[category_name] = 0
                expense_by_category[category_name] += abs(transaction.amount)


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


        report_text += "<b>💼 Состояние кошельков:</b>\n"
        for wallet in wallets:
            report_text += f"  • {wallet.name}: {wallet.value:.2f} руб.\n"

        return report_text

    except Exception as e:
        logger.error(f"Error generating report: {e}")
        return f"❌ Произошла ошибка при формировании отчета: {str(e)}"




@bot.message_handler(state=Balance_and_Reports_States.custom_period_state)
def handle_custom_period(message: Message, state: StateContext):
    try:
        user_id = message.from_user.id

        if '-' not in message.text:
            bot.send_message(message.chat.id, "❌ Неверный формат. Используйте: ДД.ММ.ГГГГ-ДД.ММ.ГГГГ")
            return

        start_str, end_str = message.text.split('-')


        start_date = datetime.strptime(start_str.strip(), "%d.%m.%Y").replace(hour=0, minute=0, second=0)
        end_date = datetime.strptime(end_str.strip(), "%d.%m.%Y").replace(hour=23, minute=59, second=59)

        if start_date > end_date:
            bot.send_message(message.chat.id, "❌ Начальная дата не может быть позже конечной")
            return


        period_days = (end_date - start_date).days + 1
        period_text = f"произвольный период ({period_days} дней)"

        report_text = generate_report(user_id, start_date, end_date, period_text)

        bot.send_message(
            chat_id=message.chat.id,
            text=report_text,
            reply_markup=keybords.back_to_reports_button(),
            parse_mode='HTML'
        )


        state.set(Balance_and_Reports_States.input_reports_state)

    except ValueError:
        bot.send_message(message.chat.id, "❌ Неверный формат даты. Используйте: ДД.ММ.ГГГГ")
    except Exception as e:
        logger.error(f"Error in custom period: {e}")
        bot.send_message(message.chat.id, "❌ Ошибка при обработке периода")






