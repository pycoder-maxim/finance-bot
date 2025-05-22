import datetime

import expense
import keybords
from telebot.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from loader import bot, db_api
from DataBaseModel import Currencies
from DataBaseModel import Wallets

# Временное хранилище введённых сумм до выбора категории.
income_amounts = {}  # user_id -> сумма



@bot.callback_query_handler(func=lambda call: True)
def answer_inc(call:CallbackQuery):
    if call.data == 'add_income':

        wallets = db_api.wallets().get_wallets_by_user_id(call.from_user.id)
        str = ""
        for wallet in wallets:
            str += wallet.name + " " + wallet.currency.name + " " + wallet.value.__str__() + "\n"

        markup = keybords.currency_account_selection()

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                  text='Выберите валюту:' + str, reply_markup=markup)




# Обработчик 1.Рубли.
# ______________________________________________________________________________________________________________________

    elif call.data == 'entering_amount_RUB':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text='Введите сумму в RUB:')
        bot.register_next_step_handler(call.message, add_db_rub)

# Обработчик 2.Доллары.
# ______________________________________________________________________________________________________________________

    elif call.data == 'entering_amount_USDT':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text='Введите сумму в USD:')
        bot.register_next_step_handler(call.message, add_db_usd)

# Обработчик 3.Евро.
# ______________________________________________________________________________________________________________________

    elif call.data == 'entering_amount_EUR':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text='Введите сумму в EUR:')
        bot.register_next_step_handler(call.message, add_db_euro)

# Обработчик 4.Вернуться назад.
# ______________________________________________________________________________________________________________________

    elif call.data == "go_to_back_menu":
        markup = keybords.go_to_menu()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text='*Финансовый бот-помощник*\n\n'
                                   'Этот бот поможет вам *оптимизировать расходы и вести учёт доходов* в течение месяца.\n\n'
                                   '*📋 Доступные команды:*\n\n'
                                   '1. *Добавить доходы* — операция дохода  \n'
                                   '2. *Добавить расходы* — операция расхода  \n'
                                   '3. *Моя статистика* — показывает статистику доходов и расходов за выбранный период  \n'
                                   '4. *Мой баланс* — текущий финансовый баланс\n\n'
                                   '*💬 Команды бота:*\n\n'
                                   '/balance — показать текущий баланс  \n'
                                   '/categories — список всех категорий  \n'
                                   '/set_category <название> [тип] — добавить новую категорию (тип = income или expense, по умолчанию expense)  \n'
                                   '/remove_category <название> — удалить существующую категорию', reply_markup=markup,
                              parse_mode='Markdown')

# Обработчик(Главное меню)5.Описание.
# ______________________________________________________________________________________________________________________

    elif call.data == "description":
        markup = keybords.go_to_menu()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text='*Финансовый бот-помощник*\n\n'
                                   'Этот бот поможет вам *оптимизировать расходы и вести учёт доходов* в течение месяца.\n\n'
                                   '*📋 Доступные команды:*\n\n'
                                   '1. *Добавить доходы* — операция дохода  \n'
                                   '2. *Добавить расходы* — операция расхода  \n'
                                   '3. *Моя статистика* — показывает статистику доходов и расходов за выбранный период  \n'
                                   '4. *Мой баланс* — текущий финансовый баланс\n\n'
                                   '*💬 Команды бота:*\n\n'
                                   '/balance — показать текущий баланс  \n'
                                   '/categories — список всех категорий  \n'
                                   '/set_category <название> [тип] — добавить новую категорию (тип = income или expense, по умолчанию expense)  \n'
                                   '/remove_category <название> — удалить существующую категорию', reply_markup=markup,
                              parse_mode='Markdown')

# Добавдление RUS RUB базу данных.
# ______________________________________________________________________________________________________________________


    #Транзакции(transactions)
def add_db_rub(messege:Message):
    user_id = messege.from_user.id
    currency_id = id(Currencies)
    wallet_id = id(Wallets)
    amount = float(messege.text)
    category = 'income'
    db_api.transactions().add_transaction(user_id=user_id,currency_id=currency_id,wallet_id=wallet_id,
                                          amount=amount,
                                          category=category,
                                          report="",
                                          date=datetime.datetime.now().__str__())
    #Валюта(currencies)
    symbol = str("₽")
    name = str("Российский рубль")
    code = str("RUB")
    """
    db_api.currencies().add_currencies(
                                       symbol=symbol,
                                       name=name,
                                       code=code)
    """
    markup = keybords.go_to_menu()
    bot.send_message(messege.chat.id, f'Доход добавлен:{amount} {symbol}',reply_markup=markup)




# Добавдление USD базу данных.
# ______________________________________________________________________________________________________________________

    #Транзакции(transactions)
def add_db_usd(messege:Message):
    user_id = messege.from_user.id
    currency_id = Currencies.id
    wallet_id = id(Wallets)
    amount = float(messege.text)
    category = 'income'
    db_api.transactions().add_transaction(user_id=user_id,currency_id=currency_id,wallet_id=wallet_id,
                                          amount=amount,
                                          category=category,
                                          report="",
                                          date=datetime.datetime.now().__str__())
    symbol = str("₽")
    name = str("Российский рубль")
    code = str("RUB")
    """
    db_api.currencies().add_currencies(
                                       symbol=symbol,
                                       name=name,
                                       code=code)
    """
    markup = keybords.go_to_menu()
    bot.send_message(messege.chat.id, f'Доход добавлен:{amount} {symbol}',reply_markup=markup)



# Добавдление EUR базу данных.
# ______________________________________________________________________________________________________________________

    # Транзакции(transactions)
def add_db_euro(messege:Message):
    user_id = messege.from_user.id
    amount = float(messege.text)
    currency_id = id(Currencies)
    wallet_id = id(Wallets)
    category = 'income'
    db_api.transactions().add_transaction(user_id=user_id,currency_id=currency_id,wallet_id=wallet_id,
                                          amount=amount,
                                          category=category,
                                          report="",
                                          date=datetime.datetime.now().__str__())
    symbol = str("₽")
    name = str("Российский рубль")
    code = str("RUB")
    """
    db_api.currencies().add_currencies(
                                       symbol=symbol,
                                       name=name,
                                       code=code)
    """
    markup = keybords.go_to_menu()
    bot.send_message(messege.chat.id, f'Доход добавлен:{amount} {symbol}', reply_markup=markup)







