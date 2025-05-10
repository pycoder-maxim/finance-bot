import telebot
from config import BOT_TOKEN
from database import *

db_api = DatabaseApi()
bot = telebot.TeleBot(BOT_TOKEN)
