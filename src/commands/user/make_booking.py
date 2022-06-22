"""
Make a booking when receiving a message like 10:00h | 22-06-13 | WOD
"""
from typing import Tuple
from telegram import Update, ReplyKeyboardRemove
from datetime import datetime

from src.use_cases.book_by_class_name import AlreadyBookedException, BookingDoesNotExistException, make_booking as make_booking_uc
from src.utils import decorators
from src.utils.telegram_context import AlphaContext


def get_date_and_class_from_message(message: str) -> Tuple[datetime, str]:
    hour, day, class_name = message.split(" | ")
    date = datetime.strptime(f"{day} {hour}", "%y-%m-%d %H:%Mh")
    return date, class_name


@decorators.user
@decorators.delete_after
async def handler(update: Update, context: AlphaContext) -> None:
    
    if (not update.effective_message) or (not context.user_email):
        return

    bot = context.bot
    chat = update.effective_message.chat_id
    message = update.effective_message.text
    
    await bot.send_chat_action(chat, "typing")
    
    date, class_name = get_date_and_class_from_message(message)

    try:
        booking = await make_booking_uc(class_name=class_name, date=date, mail=context.user_email)

        if booking.is_booked():
            await bot.send_message(chat, f"✅ Booked {date}, {class_name}", reply_markup=ReplyKeyboardRemove())
        elif booking.is_scheduled():
            await bot.send_message(chat, f"✅ Scheduled {date}, {class_name}", reply_markup=ReplyKeyboardRemove())
        else:
            await bot.send_message(chat, "❌ Something went wrong", reply_markup=ReplyKeyboardRemove())

    except BookingDoesNotExistException:
        await bot.send_message(chat, "❌ This class does not exist", reply_markup=ReplyKeyboardRemove())

    except AlreadyBookedException:
        await bot.send_message(chat, "❌ You already have this class booked", reply_markup=ReplyKeyboardRemove())

    except Exception as e:
        print(e)
        await bot.send_message(chat, "❌ Something went wrong", reply_markup=ReplyKeyboardRemove())
