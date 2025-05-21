import datetime

import expense
import keybords
from telebot.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from loader import bot, db_api
from DataBaseModel import Currencies

# Временное хранилище введённых сумм до выбора категории.
income_amounts = {}  # user_id -> сумма

@bot.message_handler(func=lambda msg: msg.text == "1. Добавить доход ♻️")
def handle_income_start(msg: Message):
    bot.send_message(msg.chat.id, "Введите сумму дохода:")
    bot.register_next_step_handler(msg, receive_income_amount)

def receive_income_amount(msg: Message):
    user_id = msg.from_user.id
    try:
        amount = float(msg.text.strip())
        income_amounts[user_id] = amount
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("Зарплата 💵", callback_data="income_salary"), # TODO - модифицировать работу с категориями дохода
            InlineKeyboardButton("Подработка ⛏️", callback_data="income_freelance")
        )
        bot.send_message(msg.chat.id, "Выберите категорию дохода:", reply_markup=markup)
    except ValueError:
        bot.send_message(msg.chat.id, "Ошибка: введите корректную сумму (например, 15000.00).")
        bot.register_next_step_handler(msg, receive_income_amount)

@bot.callback_query_handler(func=lambda call: call.data in ["income_salary", "income_freelance"])
def handle_income_category(call: CallbackQuery):
    print("da da")
    user_id = call.from_user.id
    amount = income_amounts.get(user_id)
    if amount is None:
        bot.send_message(call.message.chat.id, "Пожалуйста, сначала введите сумму дохода.")
        return

    category = "Зарплата" if call.data == "income_salary" else "Подработка"

    # Сохраняем в базу данных
    #TODO - провалидировать вызовы хендлеров базы данных, если таковых нет
    # добиавить или модифицировать таковую
    db_api.transactions().add_transaction(
        user_id=user_id,
        amount=amount,
        category=category,
        report= "",
        date= datetime.datetime.now().__str__()
    )

    bot.send_message(
        call.message.chat.id,
        f"Доход <b>{amount:.2f} руб</b> по категории <b>{category}</b> добавлен.",
        parse_mode="html"
    )

    # Очищаем временные данные
    del income_amounts[user_id]

@bot.callback_query_handler(func=lambda call: True)
def answer(call:CallbackQuery):
    if call.data == 'add income':
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
    amount = float(messege.text)
    category = 'income'
    db_api.transactions().add_transaction(user_id=user_id,currency_id=currency_id,
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
    currency_id = id(Currencies)
    amount = float(messege.text)
    category = 'income'
    db_api.transactions().add_transaction(user_id=user_id,currency_id=currency_id,
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
    category = 'income'
    db_api.transactions().add_transaction(user_id=user_id,currency_id=currency_id,
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







