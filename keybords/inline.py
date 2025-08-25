from telebot import types
from loader import db_api
from database import Currencies,Wallets, Categories

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def delete_change_the_name_create():
    markup = types.InlineKeyboardMarkup(row_width=1)
    command1 = types.InlineKeyboardButton('1. Удалить категорию 🗑', callback_data='delite_the_category')
    command2 = types.InlineKeyboardButton('2. Изменить имя категории 📌', callback_data='change_the_category')
    command3 = types.InlineKeyboardButton('3. Создать категорию 👼', callback_data='create_new_category')
    command4 = types.InlineKeyboardButton('4. Вернуться назад 🔙 ', callback_data='go_back_state_category')
    markup.add(command1, command2, command3,command4)
    return markup

def delete_change_the_wallet_create():
    markup = types.InlineKeyboardMarkup(row_width=1)
    command1 = types.InlineKeyboardButton('1. Удалить кошелек 🗑', callback_data='delite_the_wallet')
    command2 = types.InlineKeyboardButton('2. Изменить имя кошелька 📌', callback_data='change_the_wallet')
    command3 = types.InlineKeyboardButton('3. Создать кошелек 👼', callback_data='create_new_wallet')
    command4 = types.InlineKeyboardButton('4. Вернуться назад 🔙 ', callback_data='go_back_state_wallet')
    markup.add(command1, command2, command3,command4)
    return markup





def add_category_chek():
    markup = types.InlineKeyboardMarkup(row_width=1)
    command1 = types.InlineKeyboardButton('1. Дабавить категорию ', callback_data='chek_add')
    command2 = types.InlineKeyboardButton('2. Вернуться назад 🔙 ', callback_data='go_back_to_input_category')
    markup.add(command1,command2)
    return markup

def add_waltet_chek():
    markup = types.InlineKeyboardMarkup(row_width=1)
    command1 = types.InlineKeyboardButton('1. Добавить счет ', callback_data='chek_wallet_add')
    command2 = types.InlineKeyboardButton('2. Вернуться назад 🔙 ', callback_data='go_back_to_input_wallet')
    markup.add(command1,command2)
    return markup



def rename_category_chek():
    markup = types.InlineKeyboardMarkup(row_width=1)
    command1 = types.InlineKeyboardButton('1. переименовать категорию  ', callback_data='rename_add')
    command2 = types.InlineKeyboardButton('2. Вернуться назад 🔙 ', callback_data='go_back_to_input_category')
    markup.add(command1,command2)
    return markup



# Клавиатура - "Состояние транзакций/Изменения категорий"
#______________________________________________________________________________________________________________________
def transaction_status_changing_categories():
    markup = types.InlineKeyboardMarkup(row_width=1)
    command1 = types.InlineKeyboardButton('1. ✅ Создать транзакцию', callback_data='transaction_status')
    command2 = types.InlineKeyboardButton('2. 📊 Баланс и отчёты', callback_data='balance_and_reports')
    command3 = types.InlineKeyboardButton('2. 🗂 Категории', callback_data='changing_categories')
    command4 = types.InlineKeyboardButton('3. 💳 Кошельки и валюты', callback_data='changing_walets')
    markup.add(command1, command2,command3, command4)
    return markup


def after_transaction_add_markup():
    markup = types.InlineKeyboardMarkup(row_width=1)
    command1 = types.InlineKeyboardButton('1.➕ Ещё транзакцияю', callback_data='transaction_status')
    command2 = types.InlineKeyboardButton('2.📊 Баланс ', callback_data='balance_menu')
    command3 = types.InlineKeyboardButton('2. 🏠 Главное меню', callback_data='back_to_main_menu')
    markup.add(command1, command2, command3)
    return markup

#Клавиатура основного меню
#______________________________________________________________________________________________________________________
def go_to_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)
    command1 = types.InlineKeyboardButton('1. Доходы 💵', callback_data='add_income')
    command2 = types.InlineKeyboardButton('2. Расходы 🪫', callback_data='add_expense')
    command3 = types.InlineKeyboardButton('3. Сбережения 💰', callback_data='add_savings')
    command4 = types.InlineKeyboardButton('4. Цель 🎯', callback_data='add_goals')
    command5 = types.InlineKeyboardButton('5. Вернуться назад 🔙', callback_data='back_to_main_menu')
    markup.add(command1, command2, command3, command4, command5)
    return markup


# Клавиатура - "Выбор валюты."
#______________________________________________________________________________________________________________________
def currency_account_selection():
    markup = types.InlineKeyboardMarkup(row_width=1)
    currencies_list:list[Currencies] = db_api.currencies().get_all_currencies()
    buttons = [types.InlineKeyboardButton(cur.name + " " + cur.symbol, callback_data="curr_id:" + cur.id.__str__()) for cur in currencies_list]
    markup.add(*buttons)
    command4 = types.InlineKeyboardButton('⬅️ Вернуться назад 🔙 ', callback_data='go_back_state_to_wallets')
    markup.add(command4)
    return markup

def add_categories():
    markup = types.InlineKeyboardMarkup(row_width=1)
    command1 = types.InlineKeyboardButton('1. Добавить новую категорию ', callback_data='add_new_category')
    command2 = types.InlineKeyboardButton('1. Удалить существующуую категорию  ', callback_data='delete_category')
    markup.add(command1,command2)
    return markup


#_______________________________________________________________________________________________________________________
def create_wallets_markup(useer_id:int, cur_code:str):
    markup = types.InlineKeyboardMarkup(row_width=1)
    currency:Currencies = db_api.currencies().get_curreny_by_code(code=cur_code)
    wallets = db_api.wallets().get_wallets_by_user_id_and_cur_id(useer_id, currency.id)
    buttons = [types.InlineKeyboardButton(wallet.name, callback_data="wall_id:"+wallet.id.__str__()) for wallet in wallets]
    markup.add(*buttons)
    command4 = types.InlineKeyboardButton('⬅️ Вернуться назад 🔙 ', callback_data='go_back_state_to_wallets')
    markup.add(command4)
    return markup

#Клавиатура баланса и отчетов
#_______________________________________________________________________________________________________________________
def reports_and_ballance():
    markup = types.InlineKeyboardMarkup(row_width=1)
    command1 = types.InlineKeyboardButton('1. Добавить отчеты 📈', callback_data='show_reports')
    command2 = types.InlineKeyboardButton('2. назад 🔙 ', callback_data='go_to_back_menu')
    markup.add(command1, command2)
    return markup
#
#_______________________________________________________________________________________________________________________
def go_to_back():
    markup = types.InlineKeyboardMarkup(row_width=1)
    command1 = types.InlineKeyboardButton('1. Вернуться назад 🔙 ', callback_data='go_to_back_menu_fin')
    markup.add(command1)
    return markup



# Отчеты за временной период
#_______________________________________________________________________________________________________________________
def reports_time_piriod():
    markup = types.InlineKeyboardMarkup(row_width=1)
    command1 = types.InlineKeyboardButton('1. За день ', callback_data='report for the day')
    command2 = types.InlineKeyboardButton('2. За неделю ', callback_data='report for the week')
    command3 = types.InlineKeyboardButton('3. За месяц ', callback_data='report for the mounth')
    command4 = types.InlineKeyboardButton('4. За год ', callback_data='report for the year')
    markup.add(command1, command2, command3, command4)
    return markup

#_______________________________________________________________________________________________________________________
def create_categories_keyboard(list_of_cats:list[Categories]):
    markup = types.InlineKeyboardMarkup(row_width=1)
    categories_buttons = [types.InlineKeyboardButton(str(cat.name), callback_data="cat_id:"+cat.id.__str__()) for cat in list_of_cats]
    markup.add(*categories_buttons)
    command4 = types.InlineKeyboardButton('⬅️ Вернуться назад 🔙 ', callback_data='go_back_state_cat')
    markup.add(command4)
    return markup

#______________________________________________________________________________________________________________________
def create_accounts_buttons_markup(amount = None):
    markup = types.InlineKeyboardMarkup(row_width=1)
    command4 = types.InlineKeyboardButton('⬅️ Вернуться назад 🔙 ', callback_data='go_back_state')
    markup.add(command4)
    if amount is not None:
        command5 = types.InlineKeyboardButton(f'Оставить {amount} ', callback_data='set_amount')
        markup.add(command5)
    return markup

#______________________________________________________________________________________________________________________
def create_comment_transaction_state_markup(comment = None):
    markup = types.InlineKeyboardMarkup(row_width=1)
    command3 = types.InlineKeyboardButton('▶️Продолжить без комментария ▶️', callback_data='without_comment')
    markup.add(command3)
    if comment is not None:
        command3_5 = types.InlineKeyboardButton('▶️Оставить прежний ▶️', callback_data='set_comment')
        markup.add(command3_5)
    command4 = types.InlineKeyboardButton('⬅️ Вернуться назад 🔙 ', callback_data='go_back_state')
    markup.add(command4)
    return markup

#______________________________________________________________________________________________________________________
def create_finish_transaction_state_markup():
    markup = types.InlineKeyboardMarkup(row_width=1)
    command1 = types.InlineKeyboardButton('🔄 Изменить тип операции', callback_data='fin_type')
    command2 = types.InlineKeyboardButton('🗂 Изменить тип категории', callback_data='fin_cat')
    command3 = types.InlineKeyboardButton('💱 Изменить валюту операции', callback_data='fin_cur')
    command4 = types.InlineKeyboardButton('💳 Изменить счет операции', callback_data='fin_wall')
    command5 = types.InlineKeyboardButton('🔢 Изменить введенное число', callback_data='fin_amount')
    command6 = types.InlineKeyboardButton('💬 Изменить комментарий', callback_data='fin_comment')
    command7 = types.InlineKeyboardButton('✅ Готово', callback_data='fin_ok')

    markup.add(command1, command2, command3, command4, command5, command6, command7)
    return markup

"""
        type = data.get("type")
        cat_id = data.get("cat_id")
        cur_id = data.get("cur_id")
        wall_id = data.get("wall_id")
        name = data.get("type")
        report_data = data.get("comment")
        created_at = datetime.datetime.now().__str__()
        amount = data.get("amount")
"""

