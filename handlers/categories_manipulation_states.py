from telebot import types
from telebot.states import State, StatesGroup
from telebot.states.sync.context import StateContext
import datetime

from database.build.lib.DataBaseModel import Currencies, Categories, Wallets
from loader import bot, db_api
import keybords
from telebot.types import CallbackQuery


class CatStates(StatesGroup):
    category_state = State()

    change_category = State()
    category_choice = State()
    delite_category = State()
    create_category = State()
    input_new_category = State()
    final_add_category = State()

    show_category_list = State()
    input_comment_state = State()

    finish_state = State()

    change_state = State()

message_word_second_state = {"income":"дохода",
                   "expense": "расхода",
                   "saving": "сбережения",
                   "goals": "цели"
                   }

transaction_type = {"income":"доход",
                   "expense": "расход",
                   "savings": "сбережения",
                   "goals": "цель"
                   }


change_states_callbaks = ["cat", "cur", "wall", "amount", "comment"]

change_state_messages ={
    "cat"    :   "Выберете подходящую категорию",
    "cur"    :   "Выберете подходяющу валюту операвци",
    "wall"   :   "Выберете подходящий счет транзакции",
    "amount" :   "Введите сумму транзакции",
    "comment":   "Отправьте комметарий к транзакции",
}



@bot.callback_query_handler(func=lambda call: True, state=CatStates.category_state)
def menu_cat_handler(call:CallbackQuery, state: StateContext):
    if call.data == 'delite_the_category':
        markup = keybords.go_to_menu()
        state.set(CatStates.category_choice)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Выберите нужный раздел:',reply_markup=markup)


    elif call.data == 'change_the_category':
        state.set(CatStates.change_category)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Выберите категорию которую хотите изменить:')

    elif call.data == 'create_new_category':
        markup = keybords.go_to_menu()
        state.set(CatStates.create_category)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Выберите нужный раздел:',reply_markup=markup)



#create_new_category
#_______________________________________________________________________________________________________________________
@bot.callback_query_handler(func=lambda call: True, state=CatStates.create_category)
def create_category(call:CallbackQuery, state: StateContext):
    if call.data.startswith("add"):
        _, aim = call.data.split("_")
        state.add_data(**{"type":aim})
        state.set(CatStates.input_new_category)
        state.add_data(**{"message_id": call.message.id})
        state.add_data(**{"chat_id_1": call.message.chat.id})
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text='Введите название новой категории:')



@bot.message_handler(state=CatStates.input_new_category)
def input_category_state(message: types.Message, state: StateContext):
    try:
        bot.delete_message(message.chat.id, message.id)
    except Exception as err:
        print(err)
    state.add_data(**{"name": message.text})
    with state.data() as data:
        chat_id = data.get("chat_id_1")
        message_id = data.get("message_id")
        state.set(CatStates.final_add_category)
        markup = keybords.add_category_chek()
        bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                              text=f"Вы точно хотите добавить категорию: ({message.text}) ? ",reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True, state=CatStates.final_add_category)
def final_add_category(call: CallbackQuery, state: StateContext):
    if call.data == 'go_back_to_input_category':
        state.set(CatStates.category_state)
        markup = keybords.go_to_menu()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text='Выберите нужный раздел:', reply_markup=markup)
    elif call.data == 'chek_add':
        state.delete()
        with state.data() as data:
            name = data.get("name")
            ctype = data.get("type")
            created_at = datetime.datetime.now().__str__()
            markup = keybords.transaction_status_changing_categories()
            db_api.categories().create_category(name, ctype, created_at, call.from_user.id)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                  text='Категория добавленна ✅:',reply_markup=markup)



#delite_the_category
@bot.callback_query_handler(func=lambda call: True, state=CatStates.category_choice)
def add_new_catgory(call:CallbackQuery, state: StateContext):
    if call.data.startswith("add"):
        _, aim = call.data.split("_")
        state.set(CatStates.delite_category)
        state.add_data(**{"type":aim})
        list_of_categories = db_api.categories().get_categories_by_tg_id_and_ctype(call.from_user.id, aim)
        markup = keybords.create_categories_keyboard(list_of_categories)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text=f'Выберите категорию которую хотите удалить: {message_word_second_state.get(aim)}:', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True, state=CatStates.delite_category)
def change_category_delite(call:CallbackQuery, state: StateContext):
    if call.data.startswith("cat_id"):
        _, aim = call.data.split("_")
        state.set(CatStates.show_category_list)
        data, id = call.data.split(":")
        id = int(id)
        #cat_id = data.get("cat_id")
        with state.data() as data:
            type = data.get("type")
            state.add_data(**{"cat_id": id})
            db_api.categories().delete_category(id)
            list_of_categories = db_api.categories().get_categories_by_tg_id_and_ctype(call.from_user.id,type)
            markup = keybords.create_categories_keyboard(list_of_categories)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                                  text=f'Категория удаленна: {message_word_second_state.get(aim)}:',
                                  reply_markup=markup)





























