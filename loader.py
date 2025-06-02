import telebot
from config import BOT_TOKEN
from database import *
from telebot.storage import StateMemoryStorage
from telebot import custom_filters

# Initialize the bot
state_storage = StateMemoryStorage()  # don't use this in production; switch to redis
db_api = DatabaseApi()



bot = telebot.TeleBot(BOT_TOKEN, state_storage=state_storage, use_class_middlewares=True)
bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.IsDigitFilter())
bot.add_custom_filter(custom_filters.TextMatchFilter())

# necessary for state parameter in handlers.
from telebot.states.sync.middleware import StateMiddleware

bot.setup_middleware(StateMiddleware(bot))