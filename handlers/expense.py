from telebot.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from loader import bot, db_api

# Временное хранилище введённых расходов до выбора категории
expense_amounts = {}  # user_id -> сумма

@bot.message_handler(func=lambda msg: msg.text == "2. Добавить расходы 🪫")
def handle_expense_start(msg: Message):
    bot.send_message(msg.chat.id, "Введите сумму расхода:")
    bot.register_next_step_handler(msg, receive_expense_amount)

def receive_expense_amount(msg: Message):
    user_id = msg.from_user.id
    try:
        amount = float(msg.text.strip())
        expense_amounts[user_id] = amount
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("Спорт 🏀", callback_data="expense_sport"),
            InlineKeyboardButton("Развлечения 🎥", callback_data="expense_entertainment")
        )
        bot.send_message(msg.chat.id, "Выберите категорию расхода:", reply_markup=markup)
    except ValueError:
        bot.send_message(msg.chat.id, "Ошибка: введите корректную сумму (например, 250.00).")

@bot.callback_query_handler(func=lambda call: call.data in ["expense_sport", "expense_entertainment"])
def handle_expense_category(call: CallbackQuery):
    user_id = call.from_user.id
    amount = expense_amounts.get(user_id)
    if amount is None:
        bot.send_message(call.message.chat.id, "Пожалуйста, сначала введите сумму расхода.")
        return

    category = "Спорт" if call.data == "expense_sport" else "Развлечения"

    # Сохраняем в базу данных
    db_api.transactions().add(
        user_id=user_id,
        amount=amount,
        category=category,
        ttype="expense"
    )

    bot.send_message(
        call.message.chat.id,
        f"Расход <b>{amount:.2f} руб</b> по категории <b>{category}</b> добавлен.",
        parse_mode="html"
    )

    # Очищаем временные данные
    del expense_amounts[user_id]