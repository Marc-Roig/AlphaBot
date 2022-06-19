from gc import callbacks
from src.commands.user import (
    display_calendar, 
    help, 
    list_booked_classes,
    list_classes, 
    make_booking, 
    cancel_booking,
)
from src.commands.user.conversation_handlers import (
    set_token, 
    aimh_login as login
)
from src.commands.jobs import book_scheduled
from telegram.ext import (
    CommandHandler as CMH, 
    CallbackQueryHandler as CQH, 
    ConversationHandler as CH,
    MessageHandler as MGH,
    Application,
    JobQueue
)
from telegram.ext.filters import Regex
from src.utils.calendar import QH_CALENDAR_PATTERN
import datetime
from warnings import filterwarnings
from telegram.warnings import PTBUserWarning

filterwarnings(action="ignore", message=r".*CallbackQueryHandler", category=PTBUserWarning)


def add_user_commands(app: Application) -> None:
    add_handler = app.add_handler
    
    # Command handlers
    add_handler(CMH("help", help.init))
    add_handler(CMH("start", help.init))
    add_handler(CMH("calendar", display_calendar.handler))

    # Callback query handlers
    add_handler(CQH(display_calendar.handler, pattern="book"))
    add_handler(CQH(list_booked_classes.handler, pattern="list_bookings"))
    add_handler(CQH(list_classes.handler, pattern=QH_CALENDAR_PATTERN))
    add_handler(CQH(cancel_booking.confirm_cancel_h, pattern="confirm_cancel"))
    add_handler(CQH(cancel_booking.dismiss_cancel_h, pattern="dismiss_cancel"))

    # Message handlers
    add_handler(MGH(Regex("\d{2}:\d{2}h \| \d{2}-\d{2}-\d{2} \| [A-Za-z0-9_ -]+ \(BOOKED\)"), cancel_booking.handler))
    add_handler(MGH(Regex("\d{2}:\d{2}h \| \d{2}-\d{2}-\d{2} \| [A-Za-z0-9_ -]+$"), make_booking.handler))

    # Conversation handlers
    add_handler( # Set token Conversation
        CH(
            entry_points=[CMH("token", set_token.start)], # Ask for the token
            states={
                set_token.START: [MGH(Regex("^(.*?)+$"), set_token.set_token)], # Token user response
            },
            fallbacks=[CMH("cancel", set_token.cancel)],
        )
    )
    add_handler( # Login Conversation
        CH(
            entry_points=[ 
                CMH("login", login.start), # Ask for password
                CQH(login.start, pattern="login")
            ],
            states={
                login.START: [MGH(Regex("^(.*?)+$"), login.login)], # Password user response
            },
            fallbacks=[CMH("cancel", login.cancel)],
        ),
    )

def add_repeating_jobs(app: Application) -> None:

    jq: JobQueue = app.job_queue

    # Get time remaining seconds until the start of next minute plus a margin (2 seconds)
    seconds_until_next_minute = 60 - datetime.datetime.now().second + 2

    # Book scheduled classes
    jq.run_repeating(book_scheduled.handler, interval=60.0, first=seconds_until_next_minute)