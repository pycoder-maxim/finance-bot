from telebot import types
from loader import db_api
from database import Currencies,Wallets, Categories


#Клавиатура основного меню
#______________________________________________________________________________________________________________________

def go_to_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)
    command1 = types.InlineKeyboardButton('1. Доходы 💵', callback_data='add_income')
    command2 = types.InlineKeyboardButton('2. Расходы 🪫', callback_data='add_expenses')
    command3 = types.InlineKeyboardButton('3. Сбережения 💰', callback_data='add_savings')
    command4 = types.InlineKeyboardButton('4. Цель 🎯', callback_data='add_purpose')
    command5 = types.InlineKeyboardButton("5. Опиание 🖼 ",callback_data="description")
    markup.add(command1, command2, command3, command4,command5)
    return markup


# Клавиатура - "Выбор валюты."
#______________________________________________________________________________________________________________________
def currency_account_selection():
    markup = types.InlineKeyboardMarkup(row_width=1)
    command1 = types.InlineKeyboardButton('1. Рубли RUB 🇷🇺', callback_data='entering_wallett_RUB')
    command2 = types.InlineKeyboardButton('2. Доллыры USDT 🇺🇸', callback_data='entering_amount_USDT')
    command3 = types.InlineKeyboardButton('3. Евро EUR 🇪🇺 ', callback_data='entering_amount_EUR')
    command4 = types.InlineKeyboardButton('4. Вернуться назад 🔙 ', callback_data='go_back_to_menu')
    markup.add(command1, command2, command3,command4)
    return markup


# Клавиатура - "Категорий расходов."
#______________________________________________________________________________________________________________________
def categories_of_expenses():
    markup = types.InlineKeyboardMarkup(row_width=1)
    command1 = types.InlineKeyboardButton('1. Зарплата 💵', callback_data='1')
    command2 = types.InlineKeyboardButton('2. Покупки 🛒', callback_data='2')
    command3 = types.InlineKeyboardButton('3. Развлечения 🎮 ', callback_data='3')
    command4 = types.InlineKeyboardButton('4. Вернуться назад 🔙 ', callback_data='4')
    markup.add(command1, command2, command3,command4)
    return markup

#______________________________________________________________________________________________________________________
def create_wallets_markup(useer_id:int, cur_code:str):
    markup = types.InlineKeyboardMarkup(row_width=1)
    currency:Currencies = db_api.currencies().get_curreny_by_code(code=cur_code)
    wallets = db_api.wallets().get_wallets_by_user_id_and_cur_id(useer_id, currency.id)
    buttons = [types.InlineKeyboardButton(wallet.name, callback_data="wall_id:"+wallet.id.__str__()) for wallet in wallets]
    markup.add(*buttons)
    return markup

#______________________________________________________________________________________________________________________
def create_categories_keyboard(list_of_cats:list[Categories]):
    markup = types.InlineKeyboardMarkup(row_width=1)
    categories_buttons = [types.InlineKeyboardButton(cat.name, callback_data="cat_id:"+cat.id.__str__()) for cat in list_of_cats]
    markup.add(*categories_buttons)
    command4 = types.InlineKeyboardButton('⬅️ Вернуться назад 🔙 ', callback_data='go_back_to_menu')
    markup.add(command4)
    return markup
