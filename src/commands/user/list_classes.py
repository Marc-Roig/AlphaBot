from telegram import ReplyKeyboardRemove, Update, ReplyKeyboardMarkup, KeyboardButton, Bot
from datetime import datetime

from src.use_cases.list_daily_classes import list_daily_classes as list_daily_classes_uc
from src.utils.calendar import process_calendar_selection
from src.utils import decorators
from src.utils.telegram_context import AlphaContext

def create_classes_callback_data(action, date, booking_id):
    return ";".join([action, str(date), str(booking_id)])


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
        button_text += f"| {date.strftime('%y-%m-%d')} "
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
    await bot.send_chat_action(chat, "typing")

    selected_date = await process_calendar_selection(bot, update)

    if selected_date:
        classes = await _get_day_classes(selected_date, context.user_email)
        message_text = f"Select class from {selected_date.strftime('%A')} {selected_date.strftime('%d')}th"
        await bot.send_message(chat, message_text, reply_markup=classes)


@decorators.user
@decorators.delete
async def discard_booking(update: Update, context: AlphaContext) -> None:

    if (not update.effective_message) or (not context.user_email):
        return
    
    bot: Bot = context.bot
    chat = update.effective_message.chat_id

    message = await bot.send_message(chat, "Booking discarded", reply_markup=ReplyKeyboardRemove())
    await message.delete()

