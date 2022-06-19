"""

"""
from telegram import Update, Bot

from src.use_cases.list_booked_classes import list_booked_classes as list_booked_classes_uc
from src.utils import decorators
from src.utils.telegram_context import AlphaContext


async def _get_booked_classes(email: str) -> str:

    bookings = await list_booked_classes_uc(email)
    text = "Here's the list of booked classes: \n\n"
    
    for booking in bookings:
        
        if booking.is_booked():
            text += " (BOOKED)"
        
        if booking.is_scheduled():
            text += " (SCHEDULED)"

        text += f" | {booking.start_timestamp.strftime('%A %d, %H:%Mh')} | {booking.class_name}\n"

    return text


@decorators.user
async def handler(update: Update, context: AlphaContext) -> None:
    
    if (not update.effective_message) or (not context.user_email):
        return
 
    bot: Bot = context.bot
    chat = update.effective_message.chat_id
    query = update.callback_query
    
    await query.answer()
    await bot.send_chat_action(chat, "typing")

    text = await _get_booked_classes(context.user_email)
    await bot.send_message(chat, text)
