from telebot.types import  Message,CallbackQuery
from loader import bot, db_api
from telebot import types
import keybords


@bot.callback_query_handler(func=lambda call: True)
def answer(call:CallbackQuery):
    if call.data == 'A':
        wallets = db_api.wallets().get_wallets_by_user_id(call.from_user.id)
        str = ""
        for wallet in wallets:
            str += wallet.name + " " + wallet.currency + " " + wallet.value.__str__() + "\n"

        markup = keybords.time_period()

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                  text='Выберите актуальный для вас период' + str, reply_markup=markup)
    elif call.data == 'currency_account_selection':
        markup = keybords.currency_account_selection()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text='Выберете нужный счет:',reply_markup=markup)


    elif call.data == 'entering amount RUB':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text='Введите сумму:')
        bot.register_next_step_handler(call.message,add_db)


def add_db(messege):
    bot.send_message(messege.chat.id, 'Выберите категорию : <b>1.Категории доходов</b>  /  <b>2.Категории расходов</b>')


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




