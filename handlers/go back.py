from telebot import types
from telebot.types import Message, CallbackQuery

from keybords.inline import go_to_menu
from loader import bot, db_api

@bot.callback_query_handler(func=lambda call: call.data in ['go_back'])
def go_back():
        markup = types.InlineKeyboardMarkup(row_width=1)
        command1 = types.InlineKeyboardButton('1. Добавить доход ♻️', callback_data='add income')
        command2 = types.InlineKeyboardButton('2. Добавить расходы 🪫', callback_data='B')
        command3 = types.InlineKeyboardButton('3. Моя Статистика 📈', callback_data='C')
        command4 = types.InlineKeyboardButton('4. Мой баланс 💰', callback_data='D')
        markup.add(command1, command2, command3, command4)
        return markup