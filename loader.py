import telebot
from config import BOT_TOKEN
from database import *
from telebot.storage import StateMemoryStorage

# Initialize the bot
state_storage = StateMemoryStorage()  # don't use this in production; switch to redis
db_api = DatabaseApi()
bot = telebot.TeleBot(BOT_TOKEN, state_storage=state_storage, use_class_middlewares=True)
