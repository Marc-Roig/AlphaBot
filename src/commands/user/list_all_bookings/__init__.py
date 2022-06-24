from telegram.ext.filters import Regex
from telegram.ext import (
    CallbackQueryHandler as CQH, 
    Application,
)

from src.commands.user.list_all_bookings import list_all_bookings, close_list_of_bookings, refresh_list_of_bookings


def add_list_all_bookings_handlers(app: Application) -> None:

    add_handler = app.add_handler

    add_handler(CQH(list_all_bookings.handler, pattern="^list_bookings"))
    add_handler(CQH(close_list_of_bookings.handler, pattern="^close_list_bookings"))
    add_handler(CQH(refresh_list_of_bookings.handler, pattern="^refresh_list_bookings"))
