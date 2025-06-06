import telebot
from telebot import custom_filters, types
from telebot.states import State, StatesGroup
from telebot.states.sync.context import StateContext
from telebot.storage import StateMemoryStorage
from telebot.types import ReplyParameters
import datetime

from database.build.lib.DataBaseModel import Currencies, Categories, Wallets
from loader import bot, state_storage, db_api
import keybords
from telebot.types import Message, CallbackQuery

# Define states
class MyStates(StatesGroup):
    hello_state = State()
    menu_state = State()

    category_choice = State()
    currency_choice = State()
    aocount_choice = State()

    input_amount_state = State()
    input_comment_state = State()

    finish_state = State()


transaction_type = {"income":"доход",
                   "expense": "расход",
                   "savings": "сбережения",
                   "goals": "цель"
                   }

message_word_second_state = {"income":"дохода",
                   "expense": "расхода",
                   "saving": "сбережения",
                   "goals": "цели"
                   }


# Handler for name input
@bot.callback_query_handler(func=lambda call: True, state=MyStates.menu_state)
def menu_handler(call:CallbackQuery, state: StateContext):
    if call.data.startswith("add"):
        _, aim = call.data.split("_")
        state.set(MyStates.category_choice)
        state.add_data(**{"type":aim})
        list_of_categories =db_api.categories().get_categories_by_tg_id_and_ctype(call.from_user.id, aim)
        markup = keybords.create_categories_keyboard(list_of_categories)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text=f'Выберите соответствующую категорию {message_word_second_state.get(aim)}:', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True, state=MyStates.category_choice)
def name_get(call:CallbackQuery, state: StateContext):
    if call.data == 'go_back_to_menu':
        state.set(MyStates.menu_state)
        markup = keybords.go_to_menu()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                         text='Основное меню:\n Чтобы узнать доступные команды, введите /help',
                         reply_markup=markup)
    elif call.data.startswith("cat_id"):
        state.set(MyStates.currency_choice)
        data,id = call.data.split(":")
        id = int(id)
        state.add_data(**{"cat_id":id})
        markup = keybords.currency_account_selection()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text='Выберете валюту в которой будет записан доход',
                              reply_markup=markup)
    return


@bot.callback_query_handler(func=lambda call: True, state=MyStates.currency_choice)
def currency_choice_callback_get(call:CallbackQuery, state: StateContext):
    if call.data == 'go_back_state':
        state.set(MyStates.category_choice)
        list_of_income_categories = db_api.categories().get_categories_by_tg_id_and_ctype(call.from_user.id, "income")
        markup = keybords.create_categories_keyboard(list_of_income_categories)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text='Выберите категорию дохода:', reply_markup=markup)
    elif call.data.startswith("curr_id"):
        state.set(MyStates.aocount_choice)
        data,id = call.data.split(":")
        id = int(id)
        state.add_data(**{"cur_id":id})
        cur:Currencies =db_api.currencies().get_curreny_by_id(id)
        markup = keybords.create_wallets_markup(call.from_user.id, cur.code)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text='Выберете счет, на который будет записан доход',
                              reply_markup=markup)
    return


@bot.callback_query_handler(func=lambda call: True, state=MyStates.aocount_choice)
def currency_choice_callback_get(call:CallbackQuery, state: StateContext):
    if call.data == 'go_back_state':
        state.set(MyStates.currency_choice)
        markup = keybords.currency_account_selection()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text='Выберете валюту в которой будет записан доход',
                              reply_markup=markup)
    elif call.data.startswith("wall_id"):
        state.set(MyStates.input_amount_state)
        data,id = call.data.split(":")
        id = int(id)
        state.add_data(**{"wall_id":id})
        state.add_data(**{"chat_id_1":call.message.chat.id})
        state.add_data(**{"message_id":call.message.id})
        markup = keybords.create_go_back_state_button_markup()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text='Введите сумму транзакции:',
                              reply_markup=markup)
    return


@bot.callback_query_handler(func=lambda call: True, state=MyStates.input_amount_state)
def input_amount_state_back(call:CallbackQuery, state: StateContext):
    if call.data == 'go_back_state':
        state.set(MyStates.aocount_choice)
        with state.data() as data:
            cur_id = data.get("cur_id")
            cur: Currencies = db_api.currencies().get_curreny_by_id(cur_id)
            markup = keybords.create_wallets_markup(call.from_user.id, cur.code)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                text='Выберете счет, на который будет записан доход',
                                reply_markup=markup)
    return


@bot.message_handler(state=MyStates.input_amount_state, is_digit=True)
def ask_amount_transation(message: types.Message, state: StateContext):
    state.set(MyStates.input_comment_state)
    state.add_data(**{"amount":int(message.text)})
    try:
        bot.delete_message(message.chat.id, message.id)
    except Exception as err:
        print(err)

    markup = keybords.create_comment_transaction_state_markup()
    with state.data() as data:
        chat_id = data.get("chat_id_1")
        message_id = data.get("message_id")
        bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                              text='Введите комментарий к транзакции или продолжите без него, нажав на кнопку "Продолжить без комментария":',
                              reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True, state=MyStates.input_comment_state)
def input_amount_state_back(call:CallbackQuery, state: StateContext):
    print("hi")
    if call.data == 'go_back_state':
        state.set(MyStates.input_amount_state)
        markup = keybords.create_go_back_state_button_markup()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text='Введите сумму транзакции:',
                              reply_markup=markup)
    elif call.data.startswith("without_comment"):
        state.set(MyStates.finish_state)
        with state.data() as data:
            type = data.get("type")
            cat_id = data.get("cat_id")
            cur_id = data.get("cur_id")
            wall_id = data.get("wall_id")
            amount = data.get("amount")
            cat:Categories = db_api.categories().get_categories_by_id(cat_id)
            curr:Currencies = db_api.currencies().get_curreny_by_id(cur_id)
            wallet:Wallets = db_api.wallets().get_wallets_by_id(wall_id)
            trans_type_rus = transaction_type.get(type)
            print(trans_type_rus, cat_id, cur_id, wall_id, amount, cat.name, curr.name, wallet.name)
            msg = (
                f"Thank you for sharing! Here is a summary of your information:\n"
                f"Тип Транзакции - {trans_type_rus}\n"
                f"Категория - {cat.name}\n"
                f"Валюта - {curr.name}\n"
                f"Счет для транзакции - {wallet.name}\n"
                f"Колличество - {amount}"
            )
            print(msg)
            bot.send_message(call.message.chat.id,msg, parse_mode="html")
    return


@bot.message_handler(state=MyStates.input_comment_state)
def ask_amount_transation(message: types.Message, state: StateContext):
    state.set(MyStates.input_comment_state)
    state.add_data(**{"amount":int(message.text)})
    try:
        bot.delete_message(message.chat.id, message.id)
    except Exception as err:
        print(err)

    markup = keybords.create_comment_transaction_state_markup()
    with state.data() as data:
        chat_id = data.get("chat_id_1")
        message_id = data.get("message_id")
        bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                              text='Введите комментарий к транзакции или продолжите без него, нажав на кнопку "Продолжить без комментария":',
                              reply_markup=markup)

        """
        user_id = message.from_user.id
        currency: Currencies = db_api.currencies().get_curreny_by_code("RUB")
        wallet: Wallets = db_api.wallets().get_wallets_by_user_id_and_cur_id(message.from_user.id, currency.id)[1]
        category = 'income'
        amount = float(message.text)
        db_api.transactions().add_transaction(user_id=user_id, currency_id=currency.id, wallet_id=wallet.id,
                                              amount=amount,
                                              category=category,
                                              report="",
                                              date=datetime.datetime.now().__str__())
        """

@bot.callback_query_handler(func=lambda call: True, state=MyStates.finish_state)
def add_db_api(call: CallbackQuery, state: StateContext):
        state.set(MyStates.finish_state)
        list_of_transactions= db_api.transactions().add_transaction(call.from_user.id)
        markup = keybords.create_categories_keyboard(list_of_transactions)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text=f'Выберите соответствующую категорию {message_word_second_state}:',
                              reply_markup=markup)

