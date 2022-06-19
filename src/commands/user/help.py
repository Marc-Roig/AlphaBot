from typing import Any
from src.utils.menu import build_menu
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import Update
from telegram.ext import CallbackContext
from src.utils import decorators

@decorators.user
@decorators.delete
async def init(update: Update, context: CallbackContext) -> None:

    if not update.effective_message:
        return

    bot = context.bot
    chat = update.effective_message.chat_id

    # Build the help menu
    buttons = [
        InlineKeyboardButton("💪 Make Bookings", callback_data="book"),
        InlineKeyboardButton("🔐 Login", callback_data="login"),
        InlineKeyboardButton("🔎 List All Bookings", callback_data="list_bookings"),
    ]
    menu = build_menu(buttons, n_cols=2)

    # Send menu as response
    await bot.send_message(chat, "Pick one!", reply_markup=InlineKeyboardMarkup(menu))
