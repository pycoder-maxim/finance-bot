from database import Currencies,Wallets, Categories
from telebot import types
from telebot.states import State, StatesGroup
from telebot.states.sync.context import StateContext
import datetime

from database.build.lib.DataBaseModel import Currencies, Categories, Wallets
from handlers.transactions_states import MyStates
from loader import bot, db_api
import keybords
from telebot.types import CallbackQuery

class WallStates(StatesGroup):
    wallets_state = State()
    change_walets = State()
    delete_account = State()
    final_delete_state = State()
    create_wallet = State()
    create_new_name_account = State()
    final_add_wallet = State()
    rename_wallet = State()
    input_new_wallet = State()
    final_rename_wallet = State()
    wallets_state_4 = State()



@bot.callback_query_handler(func=lambda call: True, state=WallStates.wallets_state)
def menu_wall_handler(call:CallbackQuery, state: StateContext):
    if call.data == 'delite_the_wallet':
        markup = keybords.currency_account_selection()
        state.set(WallStates.change_walets)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Выберите валюту:', reply_markup=markup)

    elif call.data == 'create_new_wallet':
        markup = keybords.currency_account_selection()
        state.set(WallStates.create_wallet)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Выберите валюту:', reply_markup=markup)
    elif call.data == 'change_the_wallet':
        markup = keybords.currency_account_selection()
        state.set(WallStates.rename_wallet)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Выберите валюту:', reply_markup=markup)


    elif call.data == "go_back_state_wallet":
        state.delete()
        state.set(MyStates.start_choice)
        markup = keybords.transaction_status_changing_categories()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                         text='Выберете нужную команду',
                         reply_markup=markup)

    return


#delete_acount
#_______________________________________________________________________________________________________________________
@bot.callback_query_handler(func=lambda call: True, state=WallStates.change_walets)
def change_wallets_id(call:CallbackQuery, state: StateContext):
    if call.data.startswith("curr_id"):
        state.set(WallStates.delete_account)
        data,id = call.data.split(":")
        id = int(id)
        state.add_data(**{"cur_id":id})
        cur:Currencies =db_api.currencies().get_curreny_by_id(id)
        markup = keybords.create_wallets_markup(call.from_user.id, cur.code)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text='Выберете счет, который хотите удалить',
                              reply_markup=markup)
###
    elif call.data == 'go_back_state_to_wallets':
        markup = keybords.delete_change_the_wallet_create()
        state.set(WallStates.wallets_state)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Выберете что нужно изменить в ваших Кошельках:', reply_markup=markup)



@bot.callback_query_handler(func=lambda call: True, state=WallStates.delete_account)
def delete_acount(call:CallbackQuery, state: StateContext):
    if call.data.startswith("wall_id"):
        data, id = call.data.split(":")
        id = int(id)
        state.add_data(**{"wall_id": id})
        state.add_data(**{"chat_id_1": call.message.chat.id})
        state.add_data(**{"message_id": call.message.id})
        db_api.wallets().delete_wallet(id)
        markup = keybords.transaction_status_changing_categories()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text='Счет удален',reply_markup=markup)

        state.delete()

    elif call.data == 'go_back_state_to_wallets':
        state.set(WallStates.change_walets)
        markup = keybords.currency_account_selection()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Выберите валюту:', reply_markup=markup)


#create_acount
#_______________________________________________________________________________________________________________________
@bot.callback_query_handler(func=lambda call: True, state=WallStates.create_wallet)
def create_wallet_id(call:CallbackQuery, state: StateContext):
    if call.data.startswith("curr_id"):
        state.set(WallStates.create_new_name_account)
        data,id = call.data.split(":")
        id = int(id)
        state.add_data(**{"cur_id": id})
        state.add_data(**{"message_id": call.message.id})
        state.add_data(**{"chat_id_1": call.message.chat.id})
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text='Введите название нового счета :')


    elif call.data == 'go_back_state_to_wallets':
        markup = keybords.delete_change_the_wallet_create()
        state.set(WallStates.wallets_state)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Выберете что нужно изменить в ваших Кошельках:', reply_markup=markup)

@bot.message_handler(state=WallStates.create_new_name_account)
def input_wallet_state(message: types.Message, state: StateContext):
    try:
        bot.delete_message(message.chat.id, message.id)
    except Exception as err:
        print(err)
    state.add_data(**{"name": message.text})
    with state.data() as data:
        chat_id = data.get("chat_id_1")
        message_id = data.get("message_id")
        state.set(WallStates.final_add_wallet)
        markup = keybords.add_waltet_chek()
        bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                              text=f"Вы точно хотите добавить новый счет: ({message.text}) ? ",reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True, state=WallStates.final_add_wallet)
def final_add_wallet(call: CallbackQuery, state: StateContext):
    if call.data == 'go_back_to_input_wallet':
        markup = keybords.currency_account_selection()
        state.set(WallStates.create_wallet)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Выберите валюту:', reply_markup=markup)


    elif call.data == 'chek_wallet_add':
        with state.data() as data:
            user_id = call.from_user.id
            name = data.get("name")
            id = int(data.get("cur_id"))
            cur: Currencies = db_api.currencies().get_curreny_by_id(id)
            created_at = datetime.datetime.now().__str__()
            markup = keybords.transaction_status_changing_categories()
            db_api.wallets().create_wallet(user_id=user_id,name=name,currency=cur,created_at=created_at)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                  text='Счет добавлен ✅:',reply_markup=markup)
        state.delete()

#rename_acount
#_______________________________________________________________________________________________________________________
@bot.callback_query_handler(func=lambda call: True, state=WallStates.rename_wallet)
def change_wallets_id(call:CallbackQuery, state: StateContext):
    if call.data.startswith("curr_id"):
        state.set(WallStates.input_new_wallet)
        data,id = call.data.split(":")
        id = int(id)
        state.add_data(**{"cur_id":id})
        cur:Currencies =db_api.currencies().get_curreny_by_id(id)
        markup = keybords.create_wallets_markup(call.from_user.id, cur.code)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text='Выберете счет, который хотите переименовать',
                              reply_markup=markup)


    elif call.data == 'go_back_state_to_wallets':
        markup = keybords.delete_change_the_wallet_create()
        state.set(WallStates.wallets_state)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Выберете что нужно изменить в ваших Кошельках:', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True, state=WallStates.input_new_wallet)
def change_category_delite(call:CallbackQuery, state: StateContext):
    if call.data.startswith("wall_id"):
        state.set(WallStates.final_rename_wallet)
        data,id = call.data.split(":")
        id = int(id)
        state.add_data(**{"wall_id": id})
        state.add_data(**{"cur_id": id})
        state.add_data(**{"message_id": call.message.id})
        state.add_data(**{"chat_id_1": call.message.chat.id})
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text='Введите название нового счета :')

@bot.message_handler(state=WallStates.final_rename_wallet)
def final_rename(message: types.Message, state: StateContext):
    try:
        bot.delete_message(message.chat.id, message.id)
    except Exception as err:
        print(err)

    new_name = message.text
    state.add_data(**{"name": message.text})
    state.set(WallStates.wallets_state_4)
    with state.data() as data:
        chat_id = data.get("chat_id_1")
        message_id = data.get("message_id")
        telegram_id = data["wall_id"]
        db_api.wallets().update_wallet(telegram_id=telegram_id, name=new_name)
        print('лол')
        markup = keybords.transaction_status_changing_categories()
        bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                              text=f"Счет переименован ✅",reply_markup=markup)
    state.delete()




