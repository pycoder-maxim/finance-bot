from database import Currencies,Wallets, Categories
from telebot import types
from telebot.states import State, StatesGroup
from telebot.states.sync.context import StateContext
import datetime

from database.build.lib.DataBaseModel import Currencies, Categories, Wallets
from handlers.transactions_states import MyStates
from loader import bot, db_api
import keybords
from telebot.types import CallbackQuery

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
    if call.data == 'report for the day':
        pass
    elif call.data == 'report for the week':
        pass
    elif call.data == 'report for the mounth':
        pass
    elif call.data == 'report for the year':
        pass
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










