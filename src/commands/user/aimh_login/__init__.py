from telegram.ext.filters import Regex
from telegram.ext import (
    CommandHandler as CMH, 
    CallbackQueryHandler as CQH, 
    ConversationHandler as CH,
    MessageHandler as MGH,
    Application,
)

from src.commands.user.aimh_login import aimh_login as login


def add_login_handlers(app: Application) -> None:

    add_handler = app.add_handler

    # Login Conversation
    add_handler( 
        CH(
            entry_points=[ 
                CMH("login", login.start_handler), # Ask for password
                CQH(login.start_handler, pattern="login")
            ],
            states={
                login.START: [MGH(Regex("^(.*?)+$"), login.login_handler)], # Password user response
            },
            fallbacks=[CMH("cancel", login.cancel_handler)],
        ),
    )
