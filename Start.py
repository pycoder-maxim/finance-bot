from turtledemo.penrose import start

import telebot
from telebot import types

bot = telebot.TeleBot('7607516429:AAEpIr2Y0Xwd88iOCOLpVh1I6kC0cRgemLM')


icome = ''

@bot.message_handler(commands=['start'])
def main(messege):
    bot.send_message(messege.chat.id,'Привет, …! Я помогу вести учёт доходов и расходов. Чтобы узнать доступные команды, введите /help' )



@bot.message_handler(commands=['help'])
def info(messege):
    bot.send_message(messege.chat.id,
                     'Что-бы добавить доход введите команду /add_income И внесите: <сумма> <категория> <комментарий>**')


@bot.message_handler(commands=['add_income'])
def info(messege):
    bot.send_message(messege.chat.id,
                     f'Введите ваш доход за месяц : {icome}')

@bot.message_handler()
def ic(messege):
    if messege.text.lower() == {icome}:
        bot.send_message(messege.chat.id,
                         f'Ваш доход за месяц: {icome}')






bot.polling(none_stop=True, interval=2 )




