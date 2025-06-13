import telebot
from telebot import custom_filters, types
from telebot.states import State, StatesGroup
from telebot.states.sync.context import StateContext
from telebot.storage import StateMemoryStorage
from telebot.types import ReplyParameters
import datetime

from database.build.lib.DataBaseModel import Currencies, Categories, Wallets
from loader import bot, state_storage, db_api
import keybords
from telebot.types import Message, CallbackQuery
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP


class MyStates(StatesGroup):
    menu_state = State()
    graphics_state = State()

    @bot.message_handler(commands=['start'])
    def start(m):
        calendar, step = DetailedTelegramCalendar().build()
        bot.send_message(m.chat.id,
                         f"Select {LSTEP[step]}",
                         reply_markup=calendar)

    @bot.callback_query_handler(func=DetailedTelegramCalendar.func())
    def cal(c):
        result, key, step = DetailedTelegramCalendar().process(c.data)
        if not result and key:
            bot.edit_message_text(f"Select {LSTEP[step]}",
                                  c.message.chat.id,
                                  c.message.message_id,
                                  reply_markup=key)
        elif result:
            bot.edit_message_text(f"You selected {result}",
                                  c.message.chat.id,
                                  c.message.message_id)

