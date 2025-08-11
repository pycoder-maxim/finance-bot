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

class Balance_and_Reports(StatesGroup):
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
