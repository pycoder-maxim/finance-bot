


from database import Currencies,Wallets, Categories
from telebot import types
from telebot.states import State, StatesGroup
from telebot.states.sync.context import StateContext
import datetime

from database.build.lib.DataBaseModel import Currencies, Categories, Wallets
from loader import bot, db_api
import keybords
from telebot.types import CallbackQuery
class WallStates(StatesGroup):
    wallets_state = State()



@bot.callback_query_handler(func=lambda call: True, state=WallStates.wallets_state)
def menu_wall_handler(call:CallbackQuery, state: StateContext):
    if call.data == 'delite_the_wallet':
        user_id = call.from_user.id
        markup = keybords.create_wallets_markup(useer_id=user_id)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Выберите кошелек который хотите удалить:', reply_markup=markup)



