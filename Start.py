import telebot
from telebot.apihelper import send_message
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

import info_data
from telebot import types



bot = telebot.TeleBot('7607516429:AAEpIr2Y0Xwd88iOCOLpVh1I6kC0cRgemLM')

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
def main(messege):
    bot.send_message(messege.chat.id,'Привет, …! Я помогу вести учёт доходов и расходов. Чтобы узнать доступные команды, введите /help' )


@bot.message_handler(commands=['help'])
def info(messege):

# Меню бота (кнопки).
    markup = types.ReplyKeyboardMarkup(row_width=4, resize_keyboard=True)
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
        elif messege.text == '4. Категории 🖼️':
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




