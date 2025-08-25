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
    show_reports_state = State()
    check_ballence_state = State()

@bot.callback_query_handler(func=lambda call: True, state=Balance_and_Reports_States.begin_state)
def begin_state(call:CallbackQuery, state: StateContext):
    if call.data == 'show_reports':
        state.set(Balance_and_Reports_States.show_reports_state)
        markup = keybords.reports_time_piriod()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text='Выберите отчеты за определенный промежуток 📅',
                              reply_markup=markup)

    elif call.data == 'chek_current_balance':
        state.set(Balance_and_Reports_States.check_ballence_state)
        markup = keybords.go_to_back()
        get_ballance = db_api.wallets().get_total_balance(user_id=call.from_user.id)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text=f'Ваш текущий балланс сосотовляет: {get_ballance}',reply_markup=markup)
        state.delete()

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






