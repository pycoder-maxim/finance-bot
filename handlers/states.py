import telebot
from telebot import custom_filters, types
from telebot.states import State, StatesGroup
from telebot.states.sync.context import StateContext
from telebot.storage import StateMemoryStorage
from telebot.types import ReplyParameters
from loader import bot, state_storage
import keybords
from telebot.types import Message, CallbackQuery

# Define states
class MyStates(StatesGroup):
    hello_state = State()
    menu_state = State()

    income_type_state = State()
    expend_type_state = State()
    saving_types_state = State()
    goals_types_state = State()

    currency_choice = State()
    aocount_choice = State()

    input_amount_state = State()
    input_comment_state = State()

    finish_state = State()


# Handler for name input
@bot.callback_query_handler(func=lambda call: True, state=MyStates.menu_state)
def name_get(call:CallbackQuery, state: StateContext):
    if call.data == 'add_income':
        state.set(MyStates.income_type_state)
        markup = keybords.currency_account_selection() #TODO - сделать выбор из видов дохода
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text='Выберите тип дохода:', reply_markup=markup)
    elif call.data =='add_expenses':
        state.set(MyStates.expend_type_state)
        markup = keybords.currency_account_selection()  # TODO - сделать выбор из видов дохода
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text='Выберите тип расхода:', reply_markup=markup)
    elif call.data =='add_savings':
        state.set(MyStates.saving_types_state)
        markup = keybords.currency_account_selection()  # TODO - сделать выбор из видов дохода
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text='Выберите тип накопления:', reply_markup=markup)
    elif call.data =='add_purpose':
        state.set(MyStates.goals_types_state)
        markup = keybords.currency_account_selection()  # TODO - сделать выбор из видов дохода
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text='Выберите тип цели:', reply_markup=markup)



@bot.callback_query_handler(func=lambda call: True, state=MyStates.income_type_state)
def name_get(call:CallbackQuery, state: StateContext):
    if call.data == 'go_back_to_menu':
        state.set(MyStates.menu_state)
        markup = keybords.go_to_menu()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                         text='Основное меню:\n Чтобы узнать доступные команды, введите /help',
                         reply_markup=markup)
    return

@bot.callback_query_handler(func=lambda call: True, state=MyStates.expend_type_state)
def name_get(call:CallbackQuery, state: StateContext):
    if call.data == 'go_back_to_menu':
        state.set(MyStates.menu_state)
        markup = keybords.go_to_menu()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text='Основное меню:\n Чтобы узнать доступные команды, введите /help',
                              reply_markup=markup)
    return

@bot.callback_query_handler(func=lambda call: True, state=MyStates.saving_types_state)
def name_get(call:CallbackQuery, state: StateContext):
    if call.data == 'go_back_to_menu':
        state.set(MyStates.menu_state)
        markup = keybords.go_to_menu()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text='Основное меню:\n Чтобы узнать доступные команды, введите /help',
                              reply_markup=markup)
    return

@bot.callback_query_handler(func=lambda call: True, state=MyStates.goals_types_state)
def name_get(call:CallbackQuery, state: StateContext):
    if call.data == 'go_back_to_menu':
        state.set(MyStates.menu_state)
        markup = keybords.go_to_menu()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text='Основное меню:\n Чтобы узнать доступные команды, введите /help',
                              reply_markup=markup)
    return