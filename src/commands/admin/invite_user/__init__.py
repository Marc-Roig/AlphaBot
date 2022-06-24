from telegram.ext.filters import Regex
from telegram.ext import (
    CommandHandler as CMH, 
    CallbackQueryHandler as CQH, 
    ConversationHandler as CH,
    MessageHandler as MGH,
    Application,
)

from src.commands.user.aimh_login import aimh_login as login
from src.commands.admin.invite_user import new_user_invite

def add_user_invite_handlers(app: Application) -> None:

    add_handler = app.add_handler

    add_handler(CQH(new_user_invite.accept_invitation, pattern="^accept_invite"))
    add_handler(CQH(new_user_invite.decline_invitation, pattern="^decline_invite"))