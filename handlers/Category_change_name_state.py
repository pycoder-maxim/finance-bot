"""
from telebot import types
from telebot.states import State, StatesGroup
from telebot.states.sync.context import StateContext
import datetime

from database.build.lib.DataBaseModel import Currencies, Categories, Wallets
from loader import bot, db_api
import keybords
from telebot.types import CallbackQuery


class ChengeCatStates(StatesGroup):
    category_state = State()

    change_category = State()
    category_choice = State()
    delite_category = State()
    create_category = State()
    input_new_category = State()
    final_add_category = State()

    show_category_list = State()
    input_comment_state = State()

    finish_state = State()

    change_state = State()


message_word_second_state = {"income":"дохода",
                   "expense": "расхода",
                   "saving": "сбережения",
                   "goals": "цели"
                   }

transaction_type = {"income":"доход",
                   "expense": "расход",
                   "savings": "сбережения",
                   "goals": "цель"
                   }


change_states_callbaks = ["cat", "cur", "wall", "amount", "comment"]

change_state_messages ={
    "cat"    :   "Выберете подходящую категорию",
    "cur"    :   "Выберете подходяющу валюту операвци",
    "wall"   :   "Выберете подходящий счет транзакции",
    "amount" :   "Введите сумму транзакции",
    "comment":   "Отправьте комметарий к транзакции",
}

@bot.callback_query_handler(func=lambda call: True, state=ChengeCatStates.category_state)
def menu_cat_handler(call:CallbackQuery, state: StateContext):
    if call.data == 'change_the_category':
        state.set(ChengeCatStates.change_category)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Выберите категорию которую хотите изменить:')
"""