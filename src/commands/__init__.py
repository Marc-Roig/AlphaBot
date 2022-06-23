from src.commands.admin.conversation_handlers import (
    broadcast_all_users
)
from src.commands.user import (
    display_calendar, 
    help, 
    list_booked_classes,
    list_classes, 
    make_booking, 
    cancel_booking,
)
from src.commands.user.conversation_handlers import (
    aimh_login as login,
    new_user_invite
)
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

    # List user bookings
    add_handler(CQH(list_booked_classes.handler, pattern="^list_bookings"))

    # New user invite request
    add_handler( # Start Conversation for new users
        CH(
            entry_points=[ 
                CMH("start", new_user_invite.start), # Ask for password
            ],
            states={
                new_user_invite.START: [MGH(Regex("^(.*?)+$"), new_user_invite.send_email)], # Email address and send request to an admin
            },
            fallbacks=[CMH("cancel", new_user_invite.cancel)],
        ),
    )
    add_handler(CQH(new_user_invite.accept_invitation, pattern="^accept_invite"))
    add_handler(CQH(new_user_invite.decline_invitation, pattern="^decline_invite"))

    # Booking calendar
    add_handler(CMH("calendar", display_calendar.handler))
    add_handler(CQH(display_calendar.handler, pattern="^book"))
    add_handler(CQH(list_classes.handler, pattern="^DAY|^PREV-MONTH|^NEXT-MONTH|^IGNORE"))

    # Cancel Booking
    add_handler(MGH(Regex("\d{2}:\d{2}h \| \d{2}-\d{2}-\d{2} \| [A-Za-z0-9_ -\|\(\)\/]+ \(BOOKED\)"), cancel_booking.handler))
    add_handler(CQH(cancel_booking.confirm_cancel_h, pattern="^confirm_cancel"))
    add_handler(CQH(cancel_booking.dismiss_cancel_h, pattern="^dismiss_cancel"))

    # Make booking
    add_handler(MGH(Regex("\d{2}:\d{2}h \| \d{2}-\d{2}-\d{2} \| [A-Za-z0-9_ -\|\(\)\/]+$"), make_booking.handler))
    add_handler(MGH(Regex("^❌ Close"), list_classes.discard_booking)) # Close list of classes

    # Login Conversation
    add_handler( 
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

    # Broadcast message
    add_handler(
        CH(
            entry_points=[
                CMH("broadcast", broadcast_all_users.handler_start)
            ],
            states={
                broadcast_all_users.START: [MGH(Regex("^📣(.*?)+"), broadcast_all_users.handler_message)],
            },
            fallbacks=[CMH("cancel", broadcast_all_users.handler_cancel)],
        )
    )

def add_repeating_jobs(app: Application) -> None:

    jq: JobQueue = app.job_queue

    # Get time remaining seconds until the start of next minute plus a margin (1 second)
    seconds_until_next_minute = 60 - datetime.datetime.now().second + 1

    # Book scheduled classes
    jq.run_repeating(book_scheduled.handler, interval=60.0, first=seconds_until_next_minute)

    # Login reminder every day at 8:00 PM Europe/Madrid
    jq.run_daily(login_reminder.handler, datetime.time(20, 0, 0))
