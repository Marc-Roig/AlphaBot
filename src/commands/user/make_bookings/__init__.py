from telegram.ext.filters import Regex
from telegram.ext import (
    CommandHandler as CMH, 
    CallbackQueryHandler as CQH, 
    ConversationHandler as CH,
    MessageHandler as MGH,
    Application,
)

from src.commands.user.make_bookings import cancel_booking, display_calendar, list_classes, make_booking, discard_booking


def add_make_bookings_handlers(app: Application) -> None:

    add_handler = app.add_handler

    # Booking calendar (can be either a command or a query)
    add_handler(CMH("calendar", display_calendar.handler))
    add_handler(CQH(display_calendar.handler, pattern="^book"))

    # List classes or navigate through the calendar
    add_handler(CQH(list_classes.handler, pattern="^DAY|^PREV-MONTH|^NEXT-MONTH|^IGNORE"))

    # Cancel Booking
    add_handler(MGH(Regex("^\d{2}:\d{2}h \| [A-Za-z0-9_ -\|\(\)\/]+ (\(BOOKED\)|\(SCHEDULED\))"), cancel_booking.handler))
    add_handler(CQH(cancel_booking.confirm_cancel_h, pattern="^confirm_cancel"))
    add_handler(CQH(cancel_booking.dismiss_cancel_h, pattern="^dismiss_cancel"))

    # Make booking
    add_handler(MGH(Regex("^\d{2}:\d{2}h \| [A-Za-z0-9_ -\|\(\)\/]+$"), make_booking.handler))

    # Discard booking
    add_handler(MGH(Regex("^❌ Close"), discard_booking.handler)) # Close list of classes
