import datetime

import expense
import keybords
from telebot.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from loader import bot, db_api
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
            str += wallet.name + " " + wallet.currency + " " + wallet.value.__str__() + "\n"

        markup = keybords.time_period()

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                  text='Выберите актуальный для вас период' + str, reply_markup=markup)


# Обработчик кнопки 1.Доход за неделю.
# ______________________________________________________________________________________________________________________


    elif call.data == 'currency_account_selection_a_week':
        markup = keybords.currency_account_selection()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text='Выберете нужный счет:',reply_markup=markup)

    elif call.data == 'entering amount RUB':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text='Введите сумму:')
        bot.register_next_step_handler(call.message,add_db_rub)

    elif call.data == 'entering amount USDT':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text='Введите сумму в USD:')
        bot.register_next_step_handler(call.message, add_db_usd)

    elif call.data == 'entering amount Credit_card':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text='Введите сумму котрую хотите списать с карты:')
        bot.register_next_step_handler(call.message, add_db_credit_card)



# Обработчик кнопки 2. Доход за месяц.
#______________________________________________________________________________________________________________________
    elif call.data == 'currency_account_selection_a_mounth':
        markup = keybords.currency_account_selection()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text='Выберете нужный счет:', reply_markup=markup)

    elif call.data == 'entering amount RUB':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text='Введите сумму:')
        bot.register_next_step_handler(call.message,add_db_rub)

    elif call.data == 'entering amount USDT':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text='Введите сумму в USD:')
        bot.register_next_step_handler(call.message, add_db_usd)

    elif call.data == 'entering amount Credit_card':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text='Введите сумму котрую хотите списать с карты:')
        bot.register_next_step_handler(call.message, add_db_credit_card)



# Обработчик кнопки 3. Доход за год.
# ______________________________________________________________________________________________________________________
    elif call.data == 'currency_account_selection_a_year':
        markup = keybords.currency_account_selection()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text='Выберете нужный счет:', reply_markup=markup)

    elif call.data == 'entering amount RUB':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text='Введите сумму:')
        bot.register_next_step_handler(call.message,add_db_rub)

    elif call.data == 'entering amount USDT':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text='Введите сумму в USD:')
        bot.register_next_step_handler(call.message, add_db_usd)

    elif call.data == 'entering amount Credit_card':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text='Введите сумму котрую хотите списать с карты:')
        bot.register_next_step_handler(call.message, add_db_credit_card)


# Обработчик кнопки 4.Вернуться назад.
# ______________________________________________________________________________________________________________________


    elif call.data == "go_back":
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
                                       '/remove_category <название> — удалить существующую категорию', reply_markup=markup,parse_mode='Markdown')


# Обработчик кнопки 4.Вернуться назад к выбору временного промежутка.
# ______________________________________________________________________________________________________________________

    elif call.data == "go_back_to_time_period":
        markup = keybords.time_period()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text='Выберите актуальный для вас период', reply_markup=markup)





# Фенкции по добавления в БД.
# ______________________________________________________________________________________________________________________
# ______________________________________________________________________________________________________________________




# Добавдление RUS RUB базу данных.
# ______________________________________________________________________________________________________________________

    #Транзакции(transactions)
def add_db_rub(messege:Message):
    user_id = messege.from_user.id
    amount = float(messege.text)
    curr = messege.from_user.id
    category = 'income'
    db_api.transactions().add_transaction(user_id=user_id,curr=curr,
                                          amount=amount,
                                          category=category,
                                          report="",
                                          date=datetime.datetime.now().__str__())
    #Валюта(currencies)
    symbol = str("₽")
    name = str("Российский рубль")
    code = str("RUB")
    db_api.currencies().add_currencies(
                                       symbol=symbol,
                                       name=name,
                                       code=code)

    bot.send_message(messege.chat.id, f'Доход добавлен:{amount} {symbol}')



# Добавдление USD базу данных.
# ______________________________________________________________________________________________________________________

    #Транзакции(transactions)
def add_db_usd(messege:Message):
    user_id = messege.from_user.id
    amount = float(messege.text)
    curr = messege.from_user.id
    category = 'income'
    db_api.transactions().add_transaction(user_id=user_id,curr=curr,
                                          amount=amount,
                                          category=category,
                                          report="",
                                          date=datetime.datetime.now().__str__())
    # Валюта(currencies)
    symbol = str("$")
    name = str("Доллар США")
    code = str("USD")
    db_api.currencies().add_currencies(
                                       symbol=symbol,
                                       name=name,
                                       code=code)
    bot.send_message(messege.chat.id, f'Доход добавлен:{amount} {symbol}')


# Добавдление CR Card базу данных.
# ______________________________________________________________________________________________________________________

    # Транзакции(transactions)
def add_db_credit_card(messege:Message):
    user_id = messege.from_user.id
    amount = float(messege.text)

    category = 'income'
    db_api.transactions().add_transaction(user_id=user_id,
                                          amount=amount,
                                          category=category,
                                          report="",
                                          date=datetime.datetime.now().__str__())
    # Валюта(currencies)
    symbol = str("CR Card")
    name = str("Карта Сбер ")
    code = str("Credit_card")
    db_api.currencies().add_currencies(
                                       symbol=symbol,
                                       name=name,
                                       code=code)
    bot.send_message(messege.chat.id, f'Доход добавлен:{amount} {symbol}')
