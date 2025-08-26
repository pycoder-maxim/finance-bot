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

class Balance_and_Reports_States(StatesGroup):
    begin_state = State()
    input_reports_state = State()
    check_ballence_state = State()

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
        next_month = datetime.now().replace(day=28) + timedelta(days=4)
        end_date = next_month - timedelta(days=next_month.day)
        end_date = end_date.replace(hour=23, minute=59, second=59, microsecond=999999)
        period_text = "месяц"

    elif call.data == 'report for the year':
        start_date = datetime.now().replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        end_date = datetime.now().replace(month=12, day=31, hour=23, minute=59, second=59, microsecond=999999)
        period_text = "год"


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

    start_str = start_date.strftime("%Y-%m-%d %H:%M:%S")
    end_str = end_date.strftime("%Y-%m-%d %H:%M:%S")
    user_id = call.from_user.id
    incomes = db_api.transactions().get_by_type_period(user_id, "income", start_str, end_str)
    # Получаем расходы
    expenses = db_api.transactions().get_by_type_period(user_id, "expense", start_str, end_str)
    total_income = sum(tr.amount for tr in incomes)
    total_expense = sum(tr.amount for tr in expenses)
    balance = total_income - total_expense
    report_text = f"📊 <b>Отчет за {period_text}</b>\n\n"
    report_text += f"📅 Период: {start_date.strftime('%d.%m.%Y')} - {end_date.strftime('%d.%m.%Y')}\n\n"

    report_text += "➕ <b>Доходы:</b>\n"
    if incomes:
        for tr in incomes:
            report_text += f"   • {tr.category}: +{tr.amount:.2f} руб\n"
        report_text += f"   <b>Итого: +{total_income:.2f} руб</b>\n\n"
    else:
        report_text += "   (нет доходов)\n\n"

    report_text += "➖ <b>Расходы:</b>\n"
    if expenses:
        for tr in expenses:
            report_text += f"   • {tr.category}: -{tr.amount:.2f} руб\n"
        report_text += f"   <b>Итого: -{total_expense:.2f} руб</b>\n\n"
    else:
        report_text += "   (нет расходов)\n\n"

    report_text += f"💼 <b>Баланс: {balance:.2f} руб</b>\n\n"

    # Добавляем статус
    if balance > 0:
        report_text += "✅ Положительный баланс"
    elif balance < 0:
        report_text += "⚠️ Отрицательный баланс"
    else:
        report_text += "⚖️ Баланс сведен"

    # Отправляем отчет
    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.id,
        text=report_text,
        reply_markup=keybords.back_to_reports_button(),
        parse_mode='HTML'
    )









