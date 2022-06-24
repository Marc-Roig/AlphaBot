from telegram.ext.filters import Regex
from telegram.ext import (
    CallbackQueryHandler as CQH, 
    Application,
)

from src.commands.user.tutorials import how_to_book, how_to

def add_tutorials_handlers(app: Application) -> None:

    add_handler = app.add_handler

    add_handler(CQH(how_to.handler, pattern="^how_to_list"))
    add_handler(CQH(how_to_book.handler, pattern="^how_to_book"))
