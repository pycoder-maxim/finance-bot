from telebot.types import Message
from datetime import datetime
from loader import bot, db_api
from telebot.states.sync.context import StateContext
import keybords
from transactions_states import MyStates
from calendar_tg import DetailedTelegramCalendar, LSTEP
from datetime import date


@bot.message_handler(commands=['start'])
def main(messege: Message, state: StateContext):
    state.set(MyStates.menu_state)
    markup = keybords.go_to_menu()
    bot.send_message(messege.chat.id,
                     'Привет, …! Я помогу вести учёт доходов и расходов. Чтобы узнать доступные команды, введите /help',
                            reply_markup=markup)
    db_api.users().add_user(messege.from_user.id, messege.from_user.first_name, messege.from_user.last_name,
                            messege.from_user.username, datetime.now().__str__())


'''
@bot.message_handler(commands=['calendar'])
def start(m):
    calendar, step = DetailedTelegramCalendar().build()
    bot.send_message(m.chat.id,
                     f"Select {LSTEP[step]}",
                     reply_markup=calendar)

@bot.callback_query_handler(func=lambda call: True)
def cal(c):
    print("yes")
    result, key, step = DetailedTelegramCalendar().process(c.data)
    if not result and key:
        bot.edit_message_text(f"Select {LSTEP[step]}",
                              c.message.chat.id,
                              c.message.message_id,
                              reply_markup=key)
    elif result:
        bot.edit_message_text(f"Ваш выбор {result}",
                              c.message.chat.id,
                              c.message.message_id)

'''


@bot.message_handler(commands=['start1'])
def start(m):
    calendar, step = DetailedTelegramCalendar().build()
    bot.send_message(m.chat.id,
                     f"Select {LSTEP[step]}",
                     reply_markup=calendar)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func())
def cal(c):
    result, key, step = DetailedTelegramCalendar().process(c.data)
    if not result and key:
        bot.edit_message_text(f"Select {LSTEP[step]}",
                              c.message.chat.id,
                              c.message.message_id,
                              reply_markup=key)
    elif result:
        bot.edit_message_text(f"You selected {result}",
                              c.message.chat.id,
                              c.message.message_id)







@bot.message_handler(commands=['help'], state="*")
def info(messege):
    markup = keybords.go_to_menu()

    bot.send_message(messege.chat.id,
                     "🤖 *Финансовый бот-помощник*\n\n"
                     "Этот бот поможет вам *оптимизировать расходы и вести учёт доходов* в течение месяца.\n\n"
                     "*📋 Доступные команды:*\n\n"
                     "1. *Добавить доходы* — операция дохода  \n"
                     "2. *Добавить расходы* — операция расхода  \n"
                     "3. *Моя статистика* — показывает статистику доходов и расходов за выбранный период  \n"
                     "4. *Мой баланс* — текущий финансовый баланс\n\n"
                     "*💬 Команды бота:*\n\n"
                     "/balance — показать текущий баланс  \n"
                     "/categories — список всех категорий  \n"
                     "/set_category <название> [тип] — добавить новую категорию (тип = income или expense, по умолчанию expense)  \n"
                     "/remove_category <название> — удалить существующую категорию",
                     reply_markup=markup,
                     parse_mode='Markdown')




