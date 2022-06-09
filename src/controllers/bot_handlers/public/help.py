from typing import Any
from src.utils.menu import build_menu
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import Update


async def init(update: Update, context: Any) -> None:

    if not update.effective_chat:
        return

    bot = context.bot
    chat = update.effective_message.chat_id

    # Build the help menu
    buttons = [
        InlineKeyboardButton("🏋🏻‍♀️ Today's classes", callback_data="list_class"),
        InlineKeyboardButton("💪 Book class", callback_data="book"),
    ]
    menu = build_menu(buttons, n_cols=2)

    # Send menu as response
    bot.send_message(chat, "Pick one!", reply_markup=InlineKeyboardMarkup(menu))

