"""
Display a list of buttons of different 
features explained.
"""

from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update

from src.utils.telegram_context import AlphaContext
from src.utils import decorators
from src.utils.menu import build_menu


@decorators.user
async def handler(update: Update, context: AlphaContext) -> None:

    if (not update.effective_message):
        return

    bot: Bot = context.bot
    chat = update.effective_message.chat_id

    await bot.send_chat_action(chat, "typing")

    buttons = [
        InlineKeyboardButton("📆 Book classes", callback_data="how_to_book")
    ]  
    menu = build_menu(buttons, n_cols=1)

    await bot.send_message(
        chat, 
        (
            "*HOW TO TUTORIALS* \n\n"
            "*Click* on any of these to learn how I work"
        ),
        reply_markup=InlineKeyboardMarkup(menu),
        parse_mode="Markdown"
    )