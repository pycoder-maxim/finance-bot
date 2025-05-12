from telebot import types
from telebot.types import Message, CallbackQuery
from loader import bot, db_api
import keybords


@bot.callback_query_handler(func=lambda call: call.data in ['go_back'])
def go_back(call):
    print(call)
    markup = keybords.go_to_menu()
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                  text='Выберите актуальный для вас период' + str, reply_markup=markup)

