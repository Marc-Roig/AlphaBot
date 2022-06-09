from typing import Any
from src.controllers.bot_handlers.public import help
from telegram.ext import CommandHandler as CMH, CallbackQueryHandler as CQH, Application


def add_public_commands(app: Application) -> None:
    add_handler = app.add_handler
    add_handler(CMH("help", help.init))
