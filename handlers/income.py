import datetime
import keybords
from telebot.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from loader import bot, db_api
# Временное хранилище введённых сумм до выбора категории
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
    elif call.data == 'currency_account_selection':
        markup = keybords.currency_account_selection()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text='Выберете нужный счет:',reply_markup=markup)


    elif call.data == 'entering amount RUB':
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text='Введите сумму:')
        bot.register_next_step_handler(call.message,add_db)
    elif call.data == "go_back":
        markup = keybords.go_to_menu()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                  text='текст главного меню', reply_markup=markup)


def add_db(messege):
    bot.send_message(messege.chat.id, 'Выберите категорию : <b>1.Категории доходов</b>  /  <b>2.Категории расходов</b>')

