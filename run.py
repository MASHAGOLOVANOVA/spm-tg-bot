"""docstring for run"""
from bot.bot import bot
import commands
import auth
import ed_programme
import integration
import meeting
import menu
import project
import student
import task

print("bot runs")
bot.polling(none_stop=True, interval=0)
print("bot stopped")
