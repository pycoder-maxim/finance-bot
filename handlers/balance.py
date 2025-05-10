from telebot.types import Message
from loader import bot, db_api

@bot.message_handler(commands=["balance"])
def handle_balance(message: Message):
    user_id = message.from_user.id

    income_sum = db_api.transactions().sum_by_type(user_id, "income")
    expense_sum = db_api.transactions().sum_by_type(user_id, "expense")
    balance = income_sum - expense_sum

    text = (
        f"<b>💼 Ваш баланс</b>\n\n"
        f"➕ Доходов: <b>{income_sum:.2f} руб</b>\n"
        f"➖ Расходов: <b>{expense_sum:.2f} руб</b>\n"
        f"📊 Текущий баланс: <b>{balance:.2f} руб</b>"
    )
    bot.send_message(message.chat.id, text, parse_mode="html")