from loader import bot
import handlers.start
import handlers.income
import handlers.expense
import handlers.balance
import handlers.categories
import handlers.go_back
from builder.build_all import run_build_script
from Start import *

if __name__ == "__main__":
    bot.polling(none_stop=True)