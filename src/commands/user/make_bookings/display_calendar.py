"""
Display a calendar , when clicking on a day, a list of classes will be displayed in the keyboard for that day.
"""
from telegram import Update
from telegram.ext import CallbackContext
from src.utils.calendar import create_calendar
from src.utils import decorators
import datetime

@decorators.user
async def handler(update: Update, context: CallbackContext) -> None:
    if not update.effective_message:
        return

    bot = context.bot
    query = update.callback_query

    if query:
        await query.answer()
    
    now = datetime.datetime.now()

    await bot.send_message(update.effective_message.chat_id,
                     f"Select Day",
                     reply_markup=create_calendar(now.year, now.month))
