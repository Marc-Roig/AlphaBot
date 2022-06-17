"""
Display a calendar , when clicking on a day, a list of classes will be displayed in the keyboard for that day.
"""
from telegram import Update
from telegram.ext import CallbackContext
from src.utils.calendar import create_calendar
from src.utils import decorators


@decorators.user
async def handler(update: Update, context: CallbackContext) -> None:
    if not update.effective_message:
        return

    bot = context.bot

    await bot.send_message(update.effective_message.chat_id,
                     f"Select Day",
                     reply_markup=create_calendar(2022, 6))
