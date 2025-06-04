from loader import bot
import handlers.start
import handlers.balance
from builder.build_all import run_build_script


if __name__ == "__main__":
    bot.polling(none_stop=True)