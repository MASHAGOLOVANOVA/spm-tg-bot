"""docstring for run"""
from bot.bot import bot


print("bot runs")
bot.polling(none_stop=True, interval=0)
print("bot stopped")
