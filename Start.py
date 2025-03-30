import telebot

import info_data




bot = telebot.TeleBot('7607516429:AAEpIr2Y0Xwd88iOCOLpVh1I6kC0cRgemLM')


icome = ''

@bot.message_handler(commands=['start'])
def main(messege):
    bot.send_message(messege.chat.id,'Привет, …! Я помогу вести учёт доходов и расходов. Чтобы узнать доступные команды, введите /help' )


@bot.message_handler(commands=['help'])
def info(messege):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=4)
    command1 = types.InlineKeyboardButton('1. Добавить доход ♻️',callback_data='add_income')
    command2 = types.InlineKeyboardButton('2. Добавить расходы 🪫',callback_data='add_res')
    command3 = types.InlineKeyboardButton('3. Текущий баланс 💰',callback_data='add_m')
    command4 = types.InlineKeyboardButton('4. Категории 🖼️',callback_data='add_category')
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


@bot.callback_query_handler(func=lambda call:True)
def call_back(call):
    if call.message:
        if call.data == 'add_income':
            bot.send_message(call.messege.chat.id, 'Привет')








bot.polling(none_stop=True, interval=0 )




