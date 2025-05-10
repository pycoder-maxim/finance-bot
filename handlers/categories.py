from telebot.types import Message
from loader import bot, db_api


@bot.message_handler(commands=["categories"])
def show_categories(message: Message):
    user_id = message.from_user.id
    categories = db_api.categories().get_by_user(user_id)

    if not categories:
        bot.send_message(message.chat.id, "У вас пока нет категорий.")
        return

    income = [cat.name for cat in categories if cat.ctype == "income"]
    expense = [cat.name for cat in categories if cat.ctype == "expense"]

    text = "<b>Ваши категории:</b>\n\n"
    if income:
        text += "💵 Доходы:\n" + "\n".join(f"— {name}" for name in income) + "\n\n"
    if expense:
        text += "🪫 Расходы:\n" + "\n".join(f"— {name}" for name in expense)

    bot.send_message(message.chat.id, text, parse_mode="html")


@bot.message_handler(commands=["set_category"])
def set_category(message: Message):
    args = message.text.split(maxsplit=2)
    if len(args) < 2:
        bot.send_message(message.chat.id,
                         "Введите название категории. Пример:\n<code>/set_category Продукты expense</code>",
                         parse_mode="html")
        return

    name = args[1]
    ctype = args[2] if len(args) > 2 else "expense"
    if ctype not in ("income", "expense"):
        bot.send_message(message.chat.id, "Тип должен быть: <code>income</code> или <code>expense</code>",
                         parse_mode="html")
        return

    added = db_api.categories().add(user_id=message.from_user.id, name=name, ctype=ctype)
    if added:
        bot.send_message(message.chat.id, f"Категория <b>{name}</b> ({ctype}) добавлена.", parse_mode="html")
    else:
        bot.send_message(message.chat.id, f"Категория <b>{name}</b> уже существует.", parse_mode="html")


@bot.message_handler(commands=["remove_category"])
def remove_category(message: Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        bot.send_message(message.chat.id,
                         "Введите название категории для удаления. Пример:\n<code>/remove_category Продукты</code>",
                         parse_mode="html")
        return

    name = args[1]
    removed = db_api.categories().remove(user_id=message.from_user.id, name=name)
    if removed:
        bot.send_message(message.chat.id, f"Категория <b>{name}</b> удалена.", parse_mode="html")
    else:
        bot.send_message(message.chat.id, f"Категория <b>{name}</b> не найдена.", parse_mode="html")