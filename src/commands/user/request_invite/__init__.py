from telegram.ext.filters import Regex
from telegram.ext import (
    CommandHandler as CMH, 
    ConversationHandler as CH,
    MessageHandler as MGH,
    Application,
)

from src.commands.user.request_invite import new_user_invite


def add_request_invite_handlers(app: Application) -> None:

    add_handler = app.add_handler

    # Start Conversation for new users
    add_handler(
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