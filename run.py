"""docstring for run"""
from bot.bot import bot
import commands.command_handler
import auth.auth_handler
import integration.integration_handler
import meeting.meeting_handler
import menu.menu_handler
import project.project_handler
import student.student_handler
import task.task_handler


print("bot runs")
bot.polling(none_stop=True, interval=0)
print("bot stopped")
