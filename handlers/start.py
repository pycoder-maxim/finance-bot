import telebot
from telebot.types import Message
from database import *
from datetime import datetime
from config import BOT_TOKEN
import Keybords

db_api = DatabaseApi()
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start'])
def main(messege: Message):
    bot.send_message(messege.chat.id,
                     'Привет, …! Я помогу вести учёт доходов и расходов. Чтобы узнать доступные команды, введите /help')
    db_api.users().add_user(messege.from_user.id, messege.from_user.first_name, messege.from_user.last_name,
                            messege.from_user.username, datetime.now().__str__())


@bot.message_handler(commands=['help'])
def info(messege):
    markup = Keybords.go_to_menu()

    bot.send_message(messege.chat.id,
                     'Данный бот поможет вам оптимизировать ваши расходы с учетом ваших доходов за месяц.'
                     '\n'
                     '\nСписок команд:'
                     '\n'
                     '\n<b>1.Добавить доходы</b> - добавляет операцию «Доход»'
                     '\n'
                     '\n<b>2.Добавить расходы</b> - добавляет операцию «Расход» '
                     '\n'
                     '\n<b>3. Моя Статистика</b> - показывает статистику доходов и расходов за выбранный промежуток'
                     '\n'

                     '\n<b>4. Мой баланс</b> - показывает ваш текущий баланс'.format(messege), reply_markup=markup,
                     parse_mode='html')




