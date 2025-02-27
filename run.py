"""docstring for run"""
from commands import *
from auth import *
from ed_programme import *
from integration import *
from meeting import *
from menu import *
from project import *
from student import *
from task import *

print("bot runs")
bot.polling(none_stop=True, interval=0)
print("bot stopped")
