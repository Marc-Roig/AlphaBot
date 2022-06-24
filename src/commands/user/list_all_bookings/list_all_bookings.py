from telegram import Update, Bot

from src.use_cases.list_booked_classes import list_booked_classes as list_booked_classes_uc
from src.utils import decorators
from src.utils.telegram_context import AlphaContext
from src.utils.menu import build_menu
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

async def _get_booked_classes(email: str) -> str:

    # Get list of bookings for the user
    bookings = await list_booked_classes_uc(email)
    
    # Add list of booked classes
    text = "Your *BOOKED* classes: \n\n"

    booked_text = ""
    for booking in bookings:
        if booking.is_booked():
            booked_text += f"• {booking.start_timestamp.strftime('%A %d, %H:%Mh')} | {booking.class_name}\n"

    if booked_text:
        text += booked_text
    else:
        text += "No classes booked."


    # Add list of scheduled classes
    text += "\n Your *SCHEDULED* classes: \n\n"

    scheduled_text = ""
    for booking in bookings:
        if booking.is_scheduled():
            scheduled_text += f"• {booking.start_timestamp.strftime('%A %d, %H:%Mh')} | {booking.class_name}\n"

    if scheduled_text:
        text += scheduled_text
    else: 
        text += "No scheduled classes."

    return text

def _get_message_menu() -> list:

    buttons = [
        InlineKeyboardButton("🔄 Refresh", callback_data="refresh_list_bookings"),
        InlineKeyboardButton("❌ Close", callback_data="close_list_bookings")
    ]
    menu = build_menu(buttons, n_cols=2)

    return menu

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

    # Buttons to close and refresh list
    menu = _get_message_menu()

    await bot.send_message(chat, text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(menu))
