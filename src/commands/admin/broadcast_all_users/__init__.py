from telegram.ext.filters import Regex
from telegram.ext import (
    CommandHandler as CMH, 
    CallbackQueryHandler as CQH, 
    ConversationHandler as CH,
    MessageHandler as MGH,
    Application,
)

from src.commands.admin.broadcast_all_users import broadcast_all_users

def add_broadcast_all_users_handlers(app: Application) -> None:

    add_handler = app.add_handler

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