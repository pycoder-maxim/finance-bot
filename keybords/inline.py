from telebot import types
#Клавиатура основного меню
#______________________________________________________________________________________________________________________

def go_to_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)
    command1 = types.InlineKeyboardButton('1. Доходы 💵', callback_data='add income')
    command2 = types.InlineKeyboardButton('2. Расходы 🪫', callback_data='expenses')
    command3 = types.InlineKeyboardButton('3. Сбережения 💰', callback_data='savings')
    command4 = types.InlineKeyboardButton('4. Цель 🎯', callback_data='purpos')
    command5 = types.InlineKeyboardButton("5. Опиание 🖼 ",callback_data="description")
    markup.add(command1, command2, command3, command4,command5)
    return markup


# Клавиатура - "Выбор нужного счета"
#______________________________________________________________________________________________________________________
def currency_account_selection():
    markup = types.InlineKeyboardMarkup(row_width=1)
    command1 = types.InlineKeyboardButton('1. Рубли RUB 🇷🇺', callback_data='entering_amount_RUB')
    command2 = types.InlineKeyboardButton('2. Доллыры USDT 🇺🇸', callback_data='entering_amount_USDT')
    command3 = types.InlineKeyboardButton('3. Евро EUR 🇪🇺 ', callback_data='entering_amount_EUR')
    command4 = types.InlineKeyboardButton('4. Вернуться назад ', callback_data='go_to_back_menu')
    markup.add(command1, command2, command3,command4)
    return markup





