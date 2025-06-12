from telebot.types import Message
from datetime import datetime
from loader import bot, db_api
from telebot.states.sync.context import StateContext
import keybords
from transactions_states import MyStates


@bot.message_handler(commands=['start'])
def main(messege: Message, state: StateContext):
    state.set(MyStates.menu_state)
    markup = keybords.go_to_menu()
    bot.send_message(messege.chat.id,
                     'Привет, …! Я помогу вести учёт доходов и расходов. Чтобы узнать доступные команды, введите /help',
                            reply_markup=markup)
    db_api.users().add_user(messege.from_user.id, messege.from_user.first_name, messege.from_user.last_name,
                            messege.from_user.username, datetime.now().__str__())


@bot.message_handler(commands=['help'])
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




