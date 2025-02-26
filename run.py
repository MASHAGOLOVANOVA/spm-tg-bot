from bot.bot import bot
import commands.CommandHandler
import auth.AuthHandler
import integration.IntegrationHandler
import meeting.MeetingHandler
import menu.MenuHandler
import project.ProjectHandler
import student.StudentHandler
import task.TaskHandler
"""docstring for run"""


print("bot runs")
bot.polling(none_stop=True, interval=0)
print("bot stopped")
