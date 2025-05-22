
import datetime

import expense
import keybords
from telebot.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from loader import bot, db_api
from DataBaseModel import Currencies
from DataBaseModel import Wallets


@bot.callback_query_handler(func=lambda call: True)
def answer_exp(call:CallbackQuery):
    if call.data == 'expenses':

        markup = keybords.categories_of_expenses()

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                  text='Выберите категорию:', reply_markup=markup)

    elif call.data == '1':

        markup = keybords.currency_account_selection()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text='Введите сумму в RUB:',reply_markup=markup)

