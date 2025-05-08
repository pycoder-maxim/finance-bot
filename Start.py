import telebot
from sqlalchemy.util import bool_or_str
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, Message,CallbackQuery
from database import *
from telebot import types
from datetime import datetime


db_api = DatabaseApi()
bot = telebot.TeleBot('7607516429:AAFyO_v28qRICFTVkBtDcGar20Yge0WSa6A') #стер токен

#Переменные доходов
icome = 0

#Переменные расходов
expenditure = 0

#Переменные категорий дохода.
b = '"Зарплата"'
c = '"Подработка"'

#Переменые Категорий расхода

t = '"Спорт"'
w = '"Развлечения"'



@bot.message_handler(commands=['start'])
def main(messege:Message):
    bot.send_message(messege.chat.id,'Привет, …! Я помогу вести учёт доходов и расходов. Чтобы узнать доступные команды, введите /help' )
    db_api.users().add_user(messege.from_user.id, messege.from_user.first_name, messege.from_user.last_name,
                            messege.from_user.username, datetime.now().__str__())

@bot.message_handler(commands=['help'])
def info(messege):

# Меню бота (кнопки).
    markup = types.InlineKeyboardMarkup(row_width=1)
    command1 = types.InlineKeyboardButton('1. Добавить доход ♻️',callback_data='A')
    command2 = types.InlineKeyboardButton('2. Добавить расходы 🪫',callback_data='B')
    command3 = types.InlineKeyboardButton('3. Моя Статистика 📈',callback_data='C')
    command4 = types.InlineKeyboardButton('4. Мой баланс 💰',callback_data='D')
    markup.add(command1,command2,command3,command4)

    bot.send_message(messege.chat.id,'Данный бот поможет вам оптимизировать ваши расходы с учетом ваших доходов за месяц.'
                                     '\n'
                                     '\nСписок команд:'
                                     '\n'
                                     '\n<b>1.Добавить доходы</b> - добавляет операцию «Доход»'
                                     '\n'
                                     '\n<b>2.Добавить расходы</b> - добавляет операцию «Расход» '
                                     '\n'
                                     '\n<b>3. Моя Статистика</b> - показывает статистику доходов и расходов за выбранный промежуток'
                                     '\n'
                
                                     '\n<b>4. Мой баланс</b> - показывает ваш текущий баланс' .format(messege),reply_markup= markup, parse_mode='html')

@bot.callback_query_handler(func=lambda call: True)
def answer(call:CallbackQuery):
    if call.data == 'A':
        wallets = db_api.wallets().get_wallets_by_user_id(call.from_user.id)
        str = ""
        for wallet in wallets:
            str += wallet.name + " " + wallet.currency + " " + wallet.value.__str__() + "\n"

        markup = types.InlineKeyboardMarkup(row_width=1)
        command1 = types.InlineKeyboardButton('1. Доход за неделю ️', callback_data='I')
        command2 = types.InlineKeyboardButton('2. Доход за месяц ', callback_data='II')
        command3 = types.InlineKeyboardButton('3. Доход за год  ', callback_data='III')
        markup.add(command1, command2, command3)

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                  text='Выберите актуальный для вас период' + str, reply_markup=markup)
    elif call.data == 'I':
        markup = types.InlineKeyboardMarkup(row_width=1)
        command1 = types.InlineKeyboardButton('1. Рубли RUB 🇷🇺', callback_data='H')
        command2 = types.InlineKeyboardButton('2. Доллыры USDT 🇺🇸', callback_data='G')
        command3 = types.InlineKeyboardButton('3. Карта Сбер 💳', callback_data='F')
        markup.add(command1, command2, command3)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text='Выберете нужный счет:',reply_markup=markup)


    elif call.data == 'H':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text='Введите сумму:')
        bot.register_next_step_handler(add_db)


def add_db():
    pass




# Функционал кнопок.
@bot.message_handler(content_types=['text'])
def bot_message(messege:Message):
    if messege.chat.type == 'private':
        if messege.text == '1. Добавить доход ♻️':
            bot.send_message(messege.chat.id, 'Введите сумму дохода:' )
            bot.register_next_step_handler(messege,summa)
        elif messege.text == '2. Добавить расходы 🪫':
            bot.send_message(messege.chat.id, 'Введите сумму расхода:')
            #bot.register_next_step_handler(messege, sum_r)
        elif messege.text == '3. Моя Статистика 📈':
            wallets = db_api.wallets().get_wallets_by_user_id(messege.from_user.id)
            str = ""
            for wallet in wallets:
                str += wallet.name + " " + wallet.currency + " " + wallet.value.__str__() + "\n"
            bot.send_message(messege.chat.id, str)
            #bot.register_next_step_handler(messege,ball)
        elif messege.text == '4. Мой баланс 💰':
            bot.register_next_step_handler(messege,categ)

'''Блок обработки категорий (КНОПКА 4)'''


#Функция категорий
def categ(messege):
    markup = types.InlineKeyboardMarkup(row_width=1)
    change1 = types.InlineKeyboardButton('Категории доходов',callback_data='1')
    change2 = types.InlineKeyboardButton('Категории расходов',callback_data='2')
    markup.add(change1,change2)
    bot.send_message(messege.chat.id, 'Выберите категорию : <b>1.Категории доходов</b>  /  <b>2.Категории расходов</b>', reply_markup=markup,parse_mode='html')


@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    global icome
    if call.data == '1':
        markup_reply = types.InlineKeyboardMarkup(row_width=2)
        icome1 = types.InlineKeyboardButton('Зарплата  💵',callback_data='I')
        icome2 = types.InlineKeyboardButton('Подработка ⛏️',callback_data='II')
        icome3 = types.InlineKeyboardButton('Добавить категорию ✅',callback_data='III')
        icome4 = types.InlineKeyboardButton('Удалить категорию ❌',callback_data='IV')
        markup_reply.add(icome1,icome2,icome3,icome4,)
        bot.send_message(call.message.chat.id,'<b>Выберете категорию:</b> ',parse_mode='html',reply_markup=markup_reply)


    elif call.data == '2':
        markup_reply1 = types.InlineKeyboardMarkup(row_width=2)
        icome5 = types.InlineKeyboardButton('Спорт 🏀',callback_data='V')
        icome6 = types.InlineKeyboardButton('Развлечения 🎥',callback_data='VI')
        icome7 = types.InlineKeyboardButton('ДДобавить категорию ✅',callback_data='VII')
        icome8 = types.InlineKeyboardButton('Удалить категорию ❌',callback_data='VIII')
        markup_reply1.add(icome5,icome6,icome7,icome8)
        bot.send_message(call.message.chat.id, '<b>Выберете категорию:</b> ', parse_mode='html',
                         reply_markup=markup_reply1)

#Функционал кнопок Категорий(Зарплата, Подработка, Спорт, Развлечения)

    elif call.data == 'I':
        bot.send_message(call.message.chat.id, f'Доход <b>{icome} руб</b> по категории <b>{b}</b> добавлен',
                         parse_mode='html')
    elif call.data == 'II':
        bot.send_message(call.message.chat.id, f'Доход <b>{icome} руб</b> по категории <b>{c}</b> добавлен',
                         parse_mode='html')

    elif call.data == 'V':
        bot.send_message(call.message.chat.id, f'Расход <b>{expenditure} руб</b> по категории <b>{t}</b> добавлен',
                         parse_mode='html')

    elif call.data == 'VI':
        bot.send_message(call.message.chat.id, f'Расход <b>{expenditure} руб</b> по категории <b>{w}</b> добавлен',
                         parse_mode='html')





"""Блок обработки по балансу (КНОПКА 3). """


# Функция подсчета баланса.
def ball(messege):
    global icome
    global expenditure
    ballance = int(icome) - int(expenditure)
    bot.send_message(messege.chat.id, f'Ваш текущий балланс: <b>{ballance}</b> руб',
                     parse_mode='html')

""" Блок обработки по доходам (КНОПКА 1). """


# Функция ввести доход.

def summa(messege):
    global icome
    icome = messege.text.strip()
    bot.send_message(messege.chat.id, 'Введите комментарий:')
    bot.register_next_step_handler(messege, categ )


""" Блок обработки по расходам (КНОПКА 2). """


# Функция ввести расход.
def sum_r(messege):
    global expenditure
    expenditure = messege.text.strip()
    bot.send_message(messege.chat.id, 'Введите комментарий:')
    bot.register_next_step_handler(messege, categ )


bot.polling(none_stop=True, interval=0 )




