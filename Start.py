import telebot
from telebot.apihelper import send_message

import info_data
from telebot import types



bot = telebot.TeleBot('7607516429:AAEpIr2Y0Xwd88iOCOLpVh1I6kC0cRgemLM')

#Переменные доходов
icome = 0
category = ''
comment = ''
#Переменные расходов
expenditure = 0
category_r = ''
comment_r = ''




@bot.message_handler(commands=['start'])
def main(messege):
    bot.send_message(messege.chat.id,'Привет, …! Я помогу вести учёт доходов и расходов. Чтобы узнать доступные команды, введите /help' )


@bot.message_handler(commands=['help'])
def info(messege):

# Меню бота (кнопки).
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=4)
    command1 = types.InlineKeyboardButton('1. Добавить доход ♻️')
    command2 = types.InlineKeyboardButton('2. Добавить расходы 🪫')
    command3 = types.InlineKeyboardButton('3. Текущий баланс 💰')
    command4 = types.InlineKeyboardButton('4. Категории 🖼️')
    markup.add(command1,command2,command3,command4)

    bot.send_message(messege.chat.id,'Данный бот поможет вам оптимизировать ваши расходы с учетом ваших доходов за месяц.'
                                     '\n'
                                     '\nСписок команд:'
                                     '\n'
                                     '\n<b>1.Добавить доходы</b> - добавляет операцию «Доход»'
                                     '\n'
                                     '\n<b>2.Добавить расходы</b> - добавляет операцию «Расход» '
                                     '\n'
                                     '\n<b>3.Текущий баланс</b> - показывает текущий баланс (сумма всех доходов минус сумма всех расходов)'
                                     '\n'
                
                                     '\n<b>4.Категори</b> - выводит список доступных категорий для данного пользователя (с разделением на типы, если это предусмотрено)' .format(messege),reply_markup= markup, parse_mode='html')
# Функционал кнопок.
@bot.message_handler(content_types=['text'])
def bot_message(messege):
    if messege.chat.type == 'private':
        if messege.text == '1. Добавить доход ♻️':
            bot.send_message(messege.chat.id, 'Введите сумму дохода:' )
            bot.register_next_step_handler(messege,summa)
        elif messege.text == '2. Добавить расходы 🪫':
            bot.send_message(messege.chat.id, 'Введите сумму расхода:')
            bot.register_next_step_handler(messege, sum_r)
        elif messege.text == '3. Текущий баланс 💰':
            bot.register_next_step_handler(messege,ball)

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
    bot.send_message(messege.chat.id, 'Введите категорию дохода:')
    bot.register_next_step_handler(messege, cat)

# Функция ввести категорию дохода.
def cat(messege):
    global category
    category = messege.text.strip()
    bot.send_message(messege.chat.id, 'Введите комментарий:')
    bot.register_next_step_handler(messege, com)

# Функция ввести комментарий дохода.
def com(messege):
    global comment
    comment = messege.text.strip()
    bot.send_message(messege.chat.id, f'Доход <b>{icome} руб</b> по категории <b>{category}</b> добавлен', parse_mode='html')


""" Блок обработки по расходам (КНОПКА 2). """


# Функция ввести расход.
def sum_r(messege):
    global expenditure
    expenditure = messege.text.strip()
    bot.send_message(messege.chat.id, 'Введите категорию расхода:')
    bot.register_next_step_handler(messege, cat_r)

# Функция ввести категорию расхода.
def cat_r(messege):
    global category_r
    category_r = messege.text.strip()
    bot.send_message(messege.chat.id, 'Введите комментарий:')
    bot.register_next_step_handler(messege, com_r)

# Функция ввести комментарий расхода.
def com_r(messege):
    global comment_r
    comment_r = messege.text.strip()
    bot.send_message(messege.chat.id, f'Расход <b>{expenditure} руб</b> по категории <b>{category_r}</b> добавлен',
                     parse_mode='html')



bot.polling(none_stop=True, interval=0 )




