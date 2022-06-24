from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, Bot
from datetime import datetime

from src.use_cases.list_daily_classes import list_daily_classes as list_daily_classes_uc
from src.utils.calendar import process_calendar_selection
from src.utils import decorators
from src.utils.telegram_context import AlphaContext


def create_classes_callback_data(action, date, booking_id):
    return ";".join([action, str(date), str(booking_id)])


async def delete_last_select_message(chat_id: int, context: AlphaContext) -> None:
    """
    When user clicks on the calendar it sees:
    - A message "Select class from X day"
    - Keyboard list of classes

    After clicking on a class, the Select class message should be deleted
    to avoid clutter in the chat.
    """

    last_select_class_msg_id = context.user_data.get("select_class_message_id") # type: ignore

    if last_select_class_msg_id:
        await context.bot.delete_message(chat_id, last_select_class_msg_id)
        context.user_data["select_class_message_id"] = None # type: ignore

    return None


async def _get_day_classes(date: datetime, email: str) -> ReplyKeyboardMarkup:
    """
    Get list of classes for a single day,
    formatted as keyboard buttons.

    Ex:
    [10:00h | 22-06-13 | WOD-WEEKEND]
    [11:00h | 22-06-13 | WOD-WEEKEND]
    [12:00h | 22-06-13 | WOD-WEEKEND]

    """

    bookings = await list_daily_classes_uc(
        date,
        email,
        [
            "WOD",
            "FITCOND",
            "WOD WEEK-END",
            "FITCOND WEEK-END",
            "WEIGHTLIFTING",
            "GYMNASTICS",
        ],
    )

    text = "Here's a list of classes: \n\n"
    for booking in bookings:
        text += f" {booking.start_timestamp.strftime('%H:%M')}h - {booking.class_name} \n"

    # For each one create a button
    keyboard = []

    for booking in bookings:
        
        # Filter bookings if class ended
        if booking.end_timestamp < datetime.now():
            continue
        
        # Display time | date | class name
        button_text = f"{booking.start_timestamp.strftime('%H:%M')}h "
        # button_text += f"| {date.strftime('%y-%m-%d')} "
        button_text += f"| {booking.class_name} | {booking.get_occupation_string()} "
        
        # Mark if it's booked or scheduled
        if booking.is_booked():
            button_text += " (BOOKED)"
        elif booking.is_scheduled():
            button_text += " (SCHEDULED)"
        
        keyboard.append([
            KeyboardButton(
                button_text, 
                callback_data=create_classes_callback_data("BOOK", date, booking.id)
            )
        ])

    # Add cancel button
    keyboard.append([KeyboardButton("❌ Close", callback_data="discard_booking")])

    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

@decorators.user
async def handler(update: Update, context: AlphaContext) -> None:
    
    if (not update.effective_message) or (not context.user_email):
        return

    bot: Bot = context.bot
    chat = update.effective_message.chat_id
    query = update.callback_query
    
    await query.answer()

    selected_date = await process_calendar_selection(bot, update)

    if selected_date:
        await bot.send_chat_action(chat, "typing")

        classes = await _get_day_classes(selected_date, context.user_email)
        message_text = f"Select class from {selected_date.strftime('%A')} {selected_date.strftime('%d')}th"
        message = await bot.send_message(chat, message_text, reply_markup=classes)
        await delete_last_select_message(chat, context)

        # Store this message id in context so we can delete it when user clicks on a button
        context.user_data["select_class_message_id"] = message.message_id # type: ignore
        # Store selected date in context
        context.user_data["last_selected_date"] = selected_date # type: ignore

