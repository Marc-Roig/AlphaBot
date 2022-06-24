from src.commands.user import (
    help,
)
from src.commands.user.aimh_login import add_login_handlers
from src.commands.user.list_all_bookings import add_list_all_bookings_handlers
from src.commands.user.make_bookings import add_make_bookings_handlers
from src.commands.user.request_invite import add_request_invite_handlers
from src.commands.user.tutorials import add_tutorials_handlers

from src.commands.admin.invite_user import add_user_invite_handlers
from src.commands.admin.broadcast_all_users import add_broadcast_all_users_handlers

from src.commands.jobs import (
    book_scheduled,
    login_reminder
)
from telegram.ext import (
    CommandHandler as CMH, 
    CallbackQueryHandler as CQH, 
    ConversationHandler as CH,
    MessageHandler as MGH,
    Application,
    JobQueue
)
from telegram.ext.filters import Regex
import datetime
from warnings import filterwarnings
from telegram.warnings import PTBUserWarning


filterwarnings(action="ignore", message=r".*CallbackQueryHandler", category=PTBUserWarning)


def add_user_commands(app: Application) -> None:

    add_handler = app.add_handler
    
    # Help command to list what you can do
    add_handler(CMH("help", help.init))

    # Add all user commands
    add_list_all_bookings_handlers(app)
    add_request_invite_handlers(app)
    add_make_bookings_handlers(app)
    add_login_handlers(app)
    add_tutorials_handlers(app)


def add_admin_commands(app: Application) -> None:

    # Add all admin commands
    add_user_invite_handlers(app)
    add_broadcast_all_users_handlers(app) # Remember to add a 📣 at the start of the broadcast message


def add_repeating_jobs(app: Application) -> None:

    jq: JobQueue = app.job_queue

    # Get time remaining seconds until the start of next minute plus a margin (1 second)
    seconds_until_next_minute = 60 - datetime.datetime.now().second + 1

    # Book scheduled classes
    jq.run_repeating(book_scheduled.handler, interval=60.0, first=seconds_until_next_minute)

    # Login reminder every day at 8:00 PM Europe/Madrid
    jq.run_daily(login_reminder.handler, datetime.time(20, 0, 0))
