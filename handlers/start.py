from telebot.types import Message
from datetime import datetime
from loader import bot, db_api
from telebot.states.sync.context import StateContext
import keybords
from transactions_states import MyStates
from categories_manipulation_states import CatStates
from calendar_tg import DetailedTelegramCalendar, LSTEP
from datetime import date
from telebot.types import CallbackQuery
from wallets_manipulation import WallStates
from balance_and_report import Balance_and_Reports_States


@bot.message_handler(commands=['start'])
def main(messege: Message, state: StateContext):
    state.delete()
    state.set(MyStates.start_choice)
    markup = keybords.transaction_status_changing_categories()
    bot.send_message(messege.chat.id,
                     'Выберете нужную команду',
                            reply_markup=markup)
    db_api.users().add_user(messege.from_user.id, messege.from_user.first_name, messege.from_user.last_name,
                            messege.from_user.username, datetime.now().__str__())


@bot.callback_query_handler(func=lambda call: True)
def change_comand(call:CallbackQuery,state: StateContext):
    if call.data == 'transaction_status':
        state.set(MyStates.menu_state)
        markup = keybords.go_to_menu()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text='#Привет, …! Я помогу вести учёт доходов и расходов. Чтобы узнать доступные команды, введите /help',
                              reply_markup=markup)

    elif call.data == 'changing_categories':
        state.set(CatStates.category_state)
        markup = keybords.delete_change_the_name_create()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text='Выберете действие',
                              reply_markup=markup)
    elif call.data == 'changing_walets':
        state.set(WallStates.wallets_state)
        markup = keybords.delete_change_the_wallet_create()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text='Выберете что нужно изменить в ваших Кошельках',
                              reply_markup=markup)
    elif call.data == 'back_to_main_menu':
        markup = keybords.transaction_status_changing_categories()
        bot.send_message(call.message.chat.id,
                         'Выберете нужную команду',
                         reply_markup=markup)
        db_api.users().add_user(call.message.from_user.id, call.message.from_user.first_name, call.message.from_user.last_name,
                                call.message.from_user.username, datetime.now().__str__())
    elif call.data == 'balance_and_reports':
        state.set(Balance_and_Reports_States.begin_state)
        markup = keybords.reports_and_ballance()
        wallets = db_api.wallets().get_wallets_by_user_id(user_id=call.from_user.id)
        wallet_info = ''
        for wallet in wallets:
            wallet_info += f'{wallet.name}:  {wallet.value} руб.\n'

        bold_title = '<b>➕💼 Сумма ваших кошельков:</b>'
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text=f'{bold_title} : \n\n {wallet_info} ',
                              reply_markup=markup,parse_mode='HTML')


    else:
        result, key, step = DetailedTelegramCalendar(locale='ru').process(call.data)
        print(call.data)
        if not result and key:
            bot.edit_message_text(f"Выберете {LSTEP[step]}",
                                  call.message.chat.id,
                                  call.message.message_id,
                                  reply_markup=key)
        elif result:
            bot.edit_message_text(f"Вы выбрали{result}",
                                  call.message.chat.id,
                                  call.message.message_id)


@bot.message_handler(commands=['calendar'])
def start(m):
    calendar, step = DetailedTelegramCalendar(locale='ru').build()
    bot.send_message(m.chat.id,
                     f"Выберете {LSTEP[step]}",
                     reply_markup=calendar)



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




