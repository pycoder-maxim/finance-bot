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
    menu_state = State()

    category_choice = State()
    currency_choice = State()
    aocount_choice = State()

    input_amount_state = State()
    input_comment_state = State()

    finish_state = State()

    change_state = State()

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

change_states_callbaks = ["cat", "cur", "wall", "amount", "comment"]

change_state_messages ={
    "cat"    :   "Выберете подходящую категорию",
    "cur"    :   "Выберете подходяющу валюту операвци",
    "wall"   :   "Выберете подходящий счет транзакции",
    "amount" :   "Введите сумму транзакции",
    "comment":   "Отправьте комметарий к транзакции",
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
    if call.data == 'go_back_state':
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

        with state.data() as data:
            amount = data.get("amount")
            markup = keybords.create_accounts_buttons_markup(amount)
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
    elif call.data == "set_amount":
        state.set(MyStates.input_comment_state)
        with state.data() as data:
            comment = data.get("comment")
            markup = keybords.create_comment_transaction_state_markup(comment)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Введите комментарий к транзакции или продолжите без него или сохраните прежний, нажав на соответствующую кнопку":',
                                  reply_markup=markup)

    return


@bot.message_handler(state=MyStates.input_amount_state, is_digit=True)
def ask_amount_transation(message: types.Message, state: StateContext):
    state.set(MyStates.input_comment_state)
    state.add_data(**{"amount":float(message.text)})
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

@bot.message_handler(state=MyStates.input_amount_state, is_digit=False)
def ask_amount_transation(message: types.Message, state: StateContext):
    try:
        bot.delete_message(message.chat.id, message.id)
    except Exception as err:
        print(err)

    with state.data() as data:
        chat_id = data.get("chat_id_1")
        message_id = data.get("message_id")
        comment = data.get("comment")
        markup = keybords.create_comment_transaction_state_markup(comment)
        bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                              text='Введите корректную сумму транзакции',
                              reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True, state=MyStates.input_comment_state)
def input_amount_state_back(call:CallbackQuery, state: StateContext):

    if call.data == 'go_back_state':
        state.set(MyStates.input_amount_state)
        markup = keybords.create_accounts_buttons_markup()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text='Введите сумму транзакции:',
                              reply_markup=markup)
        return
    elif call.data.startswith("without_comment"):
        state.set(MyStates.finish_state)
        state.add_data(**{"comment":None})

    elif call.data.startswith("set_comment"):
        state.set(MyStates.finish_state)

    with state.data() as data:
        type = data.get("type")
        cat_id = data.get("cat_id")
        cur_id = data.get("cur_id")
        wall_id = data.get("wall_id")
        report_data = data.get("comment")
        created_at = datetime.datetime.now().__str__()
        amount = data.get("amount")

        cat: Categories = db_api.categories().get_categories_by_id(cat_id)
        curr: Currencies = db_api.currencies().get_curreny_by_id(cur_id)
        wallet: Wallets = db_api.wallets().get_wallets_by_id(wall_id)
        trans_type_rus = transaction_type.get(type)
        # db_api.transactions().add_transaction(message.from_user.id, type, report_data, created_at, amount,
        #                                      curr.id, wallet.id, cat.id)
        msg = (
            f"Подтвердите или исправьте даные транзакции, которые Вы ввели:\n"
            f"Тип Транзакции - {trans_type_rus}\n"
            f"Категория - {cat.name}\n"
            f"Валюта - {curr.name}\n"
            f"Счет для транзакции - {wallet.name}\n"
            f"Колличество - {amount}\n"
            f"Комментарий - {report_data}\n"
        )
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=msg,
                              reply_markup=keybords.create_finish_transaction_state_markup())
    return


@bot.message_handler(state=MyStates.input_comment_state)
def input_ask_comment(message: types.Message, state: StateContext):
    state.add_data(**{"comment":str(message.text)})
    try:
        bot.delete_message(message.chat.id, message.id)
    except Exception as err:
        print(err)
    state.set(MyStates.finish_state)
    with state.data() as data:
        type = data.get("type")
        cat_id = data.get("cat_id")
        cur_id = data.get("cur_id")
        wall_id = data.get("wall_id")
        report_data = data.get("comment")
        created_at = datetime.datetime.now().__str__()
        amount = data.get("amount")

        cat: Categories = db_api.categories().get_categories_by_id(cat_id)
        curr: Currencies = db_api.currencies().get_curreny_by_id(cur_id)
        wallet: Wallets = db_api.wallets().get_wallets_by_id(wall_id)
        trans_type_rus = transaction_type.get(type)
        #db_api.transactions().add_transaction(message.from_user.id, type, report_data, created_at, amount,
        #                                      curr.id, wallet.id, cat.id)
        msg = (
            f"Подтвердите или исправьте даные транзакции, которые Вы ввели:\n"
            f"Тип Транзакции - {trans_type_rus}\n"
            f"Категория - {cat.name}\n"
            f"Валюта - {curr.name}\n"
            f"Счет для транзакции - {wallet.name}\n"
            f"Колличество - {amount}\n"
            f"Комментарий - {report_data}\n"
        )
        chat_id = data.get("chat_id_1")
        message_id = data.get("message_id")
        bot.edit_message_text(chat_id=chat_id,
                              message_id=message_id,
                              text=msg,
                              reply_markup=keybords.create_finish_transaction_state_markup())



# Реализация finish_state хендлера
@bot.callback_query_handler(func=lambda call: True, state=MyStates.finish_state)
def finish_state_callback(call: CallbackQuery, state: StateContext):
    if call.data == "fin_ok":
        with state.data() as data:
            type = data.get("type")
            cat_id = data.get("cat_id")
            cur_id = data.get("cur_id")
            wall_id = data.get("wall_id")
            name = data.get("type")
            report_data = data.get("comment")
            created_at = datetime.datetime.now().__str__()
            amount = data.get("amount")

            cat: Categories = db_api.categories().get_categories_by_id(cat_id)
            curr: Currencies = db_api.currencies().get_curreny_by_id(cur_id)
            wallet: Wallets = db_api.wallets().get_wallets_by_id(wall_id)
            trans_type_rus = transaction_type.get(type)
            db_api.transactions().add_transaction(call.message.from_user.id, name, report_data, created_at, amount,
                                                  int(cur_id), int(wall_id), int(cat_id))

            markup = keybords.go_to_menu()
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.id,
                text="✅ Транзакция успешно сохранена!",
                reply_markup=markup
            )

            state.set(MyStates.menu_state)
            return
    elif call.data.startswith("fin_"):
        _, aim_data = call.data.split("_")
        if aim_data == "type":
            state.set(MyStates.menu_state)
            markup = keybords.go_to_menu()
            bot.edit_message_text(call.message.chat.id, call.message.id,
                             text='При изменении Типа операции необходимо ввести все данные заного',
                             reply_markup=markup)
            return
        elif aim_data == "cat":
            state.set(MyStates.change_state)
            state.add_data(**{"change_state":"cat"})
            with state.data() as data:
                type = data.get("type")
                list_of_categories = db_api.categories().get_categories_by_tg_id_and_ctype(call.from_user.id, type)
                markup = keybords.create_categories_keyboard(list_of_categories)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                      text=change_state_messages[aim_data], reply_markup=markup)
        elif aim_data == "cur":
            state.set(MyStates.currency_choice)
            markup = keybords.currency_account_selection()
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                  text=change_state_messages[aim_data], reply_markup=markup)
        elif aim_data == "wall":
            with state.data() as data:
                cur_id = data.get("cur_id")
                cur: Currencies = db_api.currencies().get_curreny_by_id(cur_id)
                markup = keybords.create_wallets_markup(call.from_user.id, cur.code)
            state.set(MyStates.aocount_choice)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                  text=change_state_messages[aim_data], reply_markup=markup)
        elif aim_data == "amount":
            state.set(MyStates.change_state)
            state.add_data(**{"change_state":"amount"})
            with state.data() as data:
                amount = data.get("amount")
                markup = keybords.create_accounts_buttons_markup(amount)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                  text=change_state_messages[aim_data], reply_markup=markup)
        elif aim_data == "comment":
            state.set(MyStates.change_state)
            state.add_data(**{"change_state": "comment"})
            with state.data() as data:
                markup = keybords.create_comment_transaction_state_markup(data.get("comment"))
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                  text=change_state_messages[aim_data], reply_markup=markup)


# Реализация change_state хендлера
@bot.callback_query_handler(func=lambda call: True, state=MyStates.change_state)
def change_state_callback(call: CallbackQuery, state: StateContext):
    with state.data() as data:
        state_changing = data.get("change_state")
        if state_changing == "cat":
            print(call.data)
            if call.data.startswith("cat_id"):
                state.set(MyStates.finish_state)
                _, id = call.data.split(":")
                id = int(id)
                data["cat_id"] = id
        elif state_changing == "comment":
            if call.data.startswith("without_comment"):
                state.set(MyStates.finish_state)
                data["comment"] = None
            elif call.data.startswith("set_comment") or call.data.startswith("go_back_state"):
                state.set(MyStates.finish_state)
        elif state_changing == "amount":
            if call.data.startswith("set_amount") or call.data.startswith("go_back_state"):
                state.set(MyStates.finish_state)

        type = data.get("type")
        cat_id = data.get("cat_id")
        cur_id = data.get("cur_id")
        wall_id = data.get("wall_id")
        report_data = data.get("comment")
        created_at = datetime.datetime.now().__str__()
        amount = data.get("amount")

        cat: Categories = db_api.categories().get_categories_by_id(cat_id)
        curr: Currencies = db_api.currencies().get_curreny_by_id(cur_id)
        wallet: Wallets = db_api.wallets().get_wallets_by_id(wall_id)
        trans_type_rus = transaction_type.get(type)
        # db_api.transactions().add_transaction(message.from_user.id, type, report_data, created_at, amount,
        #                                      curr.id, wallet.id, cat.id)
        msg = (
            f"Подтвердите или исправьте даные транзакции, которые Вы ввели:\n"
            f"Тип Транзакции - {trans_type_rus}\n"
            f"Категория - {cat.name}\n"
            f"Валюта - {curr.name}\n"
            f"Счет для транзакции - {wallet.name}\n"
            f"Колличество - {amount}\n"
            f"Комментарий - {report_data}\n"
        )
        chat_id = data.get("chat_id_1")
        message_id = data.get("message_id")
        bot.edit_message_text(chat_id=chat_id,
                              message_id=message_id,
                              text=msg,
                              reply_markup=keybords.create_finish_transaction_state_markup())



@bot.message_handler(state=MyStates.change_state,is_digit=False)
def input_ask_comment(message: types.Message, state: StateContext):
    try:
        bot.delete_message(message.chat.id, message.id)
    except Exception as err:
        print(err)

    with state.data() as data:
        state_changing = data.get("change_state")
        if state_changing == "comment":
            state.set(MyStates.finish_state)
            data["comment"] = str(message.text)
        if state_changing == "amount":
            chat_id = data.get("chat_id_1")
            message_id = data.get("message_id")
            amount = data.get("amount")
            markup = keybords.create_accounts_buttons_markup(amount)
            bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text="Введите корректную сумму транзакции",
                                  reply_markup=markup)
            return

        type = data.get("type")
        cat_id = data.get("cat_id")
        cur_id = data.get("cur_id")
        wall_id = data.get("wall_id")
        report_data = data.get("comment")
        created_at = datetime.datetime.now().__str__()
        amount = data.get("amount")

        cat: Categories = db_api.categories().get_categories_by_id(cat_id)
        curr: Currencies = db_api.currencies().get_curreny_by_id(cur_id)
        wallet: Wallets = db_api.wallets().get_wallets_by_id(wall_id)
        trans_type_rus = transaction_type.get(type)
        # db_api.transactions().add_transaction(message.from_user.id, type, report_data, created_at, amount,
        #                                      curr.id, wallet.id, cat.id)
        msg = (
            f"Подтвердите или исправьте даные транзакции, которые Вы ввели:\n"
            f"Тип Транзакции - {trans_type_rus}\n"
            f"Категория - {cat.name}\n"
            f"Валюта - {curr.name}\n"
            f"Счет для транзакции - {wallet.name}\n"
            f"Колличество - {amount}\n"
            f"Комментарий - {report_data}\n"
        )
        chat_id = data.get("chat_id_1")
        message_id = data.get("message_id")
        bot.edit_message_text(chat_id=chat_id,
                              message_id=message_id,
                              text=msg,
                              reply_markup=keybords.create_finish_transaction_state_markup())


@bot.message_handler(state=MyStates.change_state,is_digit=True)
def input_ask_comment(message: types.Message, state: StateContext):
    try:
        bot.delete_message(message.chat.id, message.id)
    except Exception as err:
        print(err)

    with state.data() as data:
        state_changing = data.get("change_state")
        if state_changing == "comment":
            state.set(MyStates.finish_state)
            data["comment"] = str(message.text)
        if state_changing == "amount":
            state.set(MyStates.finish_state)
            data["amount"] = float(message.text)

        type = data.get("type")
        cat_id = data.get("cat_id")
        cur_id = data.get("cur_id")
        wall_id = data.get("wall_id")
        report_data = data.get("comment")
        created_at = datetime.datetime.now().__str__()
        amount = data.get("amount")

        cat: Categories = db_api.categories().get_categories_by_id(cat_id)
        curr: Currencies = db_api.currencies().get_curreny_by_id(cur_id)
        wallet: Wallets = db_api.wallets().get_wallets_by_id(wall_id)
        trans_type_rus = transaction_type.get(type)
        # db_api.transactions().add_transaction(message.from_user.id, type, report_data, created_at, amount,
        #                                      curr.id, wallet.id, cat.id)
        msg = (
            f"Подтвердите или исправьте даные транзакции, которые Вы ввели:\n"
            f"Тип Транзакции - {trans_type_rus}\n"
            f"Категория - {cat.name}\n"
            f"Валюта - {curr.name}\n"
            f"Счет для транзакции - {wallet.name}\n"
            f"Колличество - {amount}\n"
            f"Комментарий - {report_data}\n"
        )
        chat_id = data.get("chat_id_1")
        message_id = data.get("message_id")
        bot.edit_message_text(chat_id=chat_id,
                              message_id=message_id,
                              text=msg,
                              reply_markup=keybords.create_finish_transaction_state_markup())
