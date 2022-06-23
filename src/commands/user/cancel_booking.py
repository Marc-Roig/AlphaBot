"""
Make a booking when receiving a message like 10:00h | 22-06-13 | WOD
"""
from typing import Tuple
from telegram import Update, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup

from datetime import datetime

from src.use_cases.cancel_booking import BookingDoesNotExistException, NotBookedException, cancel_booking as cancel_booking_uc
from src.utils import decorators
from src.utils.menu import build_menu
from src.utils.telegram_context import AlphaContext


def get_date_and_class_from_message(message: str) -> Tuple[datetime, str]:
    hour, day, class_name, _ = message.split(" | ")
    date = datetime.strptime(f"{day} {hour}", "%y-%m-%d %H:%Mh")
    return date, class_name.removesuffix(' (BOOKED)')


@decorators.user
@decorators.delete_after
async def handler(update: Update, context: AlphaContext) -> None:
    
    if (not update.effective_message) or (not context.user_email):
        return

    bot = context.bot
    chat = update.effective_message.chat_id
    message = update.effective_message.text
    await bot.send_chat_action(chat, "typing")
    
    # Store message in context for later use
    context.user_data["booking"] = message # type: ignore

    # Ask user if its sure he wants to cancel the booking
    buttons = [
        InlineKeyboardButton("No", callback_data="dismiss_cancel"),
        InlineKeyboardButton("Yes", callback_data="confirm_cancel"),
    ]
    menu = build_menu(buttons, n_cols=2)
    await bot.send_message(chat, f"Sure you want to cancel [{message}]", reply_markup=InlineKeyboardMarkup(menu))


@decorators.user
@decorators.delete_after
async def confirm_cancel_h(update: Update, context: AlphaContext) -> None:
    
    if (not update.effective_message) or (not context.user_email):
        return

    bot = context.bot
    chat = update.effective_message.chat_id
    query = update.callback_query
    
    await query.answer()
    await bot.send_chat_action(chat, "typing")

    try:
        # Get the booking date and class name from context
        booking_message = context.user_data.get('booking') # type: ignore
        date, class_name = get_date_and_class_from_message(booking_message)

        booking = await cancel_booking_uc(class_name=class_name, date=date, mail=context.user_email)

        if booking.is_booked() or booking.is_scheduled():
            await bot.send_message(chat, "❌ Something went wrong", reply_markup=ReplyKeyboardRemove())
        else:
            await bot.send_message(chat, f"✅ Canceled {date}, {class_name}", reply_markup=ReplyKeyboardRemove())

    except BookingDoesNotExistException:
        await bot.send_message(chat, "❌ This class does not exist", reply_markup=ReplyKeyboardRemove())

    except NotBookedException:
        await bot.send_message(chat, "❌ This class was not booked", reply_markup=ReplyKeyboardRemove())

    except Exception as e:
        print(e)
        await bot.send_message(chat, "❌ Something went wrong", reply_markup=ReplyKeyboardRemove())
    

@decorators.user
@decorators.delete
async def dismiss_cancel_h(update: Update, context: AlphaContext) -> None:
    
    if (not update.effective_message):
        return

    bot = context.bot
    chat = update.effective_message.chat_id
    query = update.callback_query
    
    await query.answer()
