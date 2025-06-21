from telebot import types
from telebot.states import State, StatesGroup
from telebot.states.sync.context import StateContext
import datetime

from database.build.lib.DataBaseModel import Currencies, Categories, Wallets
from loader import bot, db_api
import keybords
from telebot.types import CallbackQuery


class CatStates(StatesGroup):
    category_state = State()

    change_category = State()
    category_choice = State()
    currency_choice = State()
    aocount_choice = State()

    input_amount_state = State()
    input_comment_state = State()

    finish_state = State()

    change_state = State()

message_word_second_state = {"income":"дохода",
                   "expense": "расхода",
                   "saving": "сбережения",
                   "goals": "цели"
                   }


@bot.callback_query_handler(func=lambda call: True, state=CatStates.category_state)
def menu_cat_handler(call:CallbackQuery, state: StateContext):
    if call.data.startswith("add"):
        _, aim = call.data.split("_")
        state.set(CatStates.category_choice)
        state.add_data(**{"type": aim})
        list_of_categories = db_api.categories().get_categories_by_tg_id_and_ctype(call.from_user.id, aim)
        markup = keybords.create_categories_keyboard(list_of_categories)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text=f'Выберите соответствующую категорию {message_word_second_state.get(aim)}:',
                              reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True, state=CatStates.category_choice)
def cat_get(call:CallbackQuery, state: StateContext):
    pass




