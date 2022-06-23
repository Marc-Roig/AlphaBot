"""
Cron to book scheduled classes.
"""
from telegram.ext import CallbackContext
from src.output_ports.telegram_user_port import TelegramUser
from src.use_cases.book_user_scheduled_classes import make_bookings
from src.infrastructure import user_repository, telegram_user_repository
import asyncio


async def _make_user_bookings(context: CallbackContext, user_email: str) -> None:
    
    # Make bookings for the user. It returns a list of bookings that were scheduled for the user.
    bookings_promises = await make_bookings(user_email)
    bookings = await asyncio.gather(*bookings_promises)

    # Get the telegram user before notifying the user
    telegram_user = await telegram_user_repository.get_user_by_email(user_email)
    if not telegram_user:
        return

    # For each scheduled booking, check if it has been booked / canceled
    # and notify the user
    for booking in bookings:
        if not booking:
            continue

        if booking.is_canceled():
            await context.bot.send_message(
                telegram_user.id, 
                f"🤖❌ Booking discarded *{booking.class_name} - {booking.start_timestamp.strftime('%A %d. %H:%M')}*. Something went wrong",
                parse_mode="Markdown"
            )
            
        if booking.is_booked():
            await context.bot.send_message(
                telegram_user.id, 
                f"🤖✅ Booked *{booking.class_name} - {booking.start_timestamp.strftime('%A %d. %H:%M')}h*",
                parse_mode='Markdown'
            )


async def handler(context: CallbackContext) -> None:
    
    users = await user_repository.get_all()
    bookings_promises = []

    # Make all bookings
    for user in users:
        bookings_promises.append(_make_user_bookings(context, user.email))

    await asyncio.gather(*bookings_promises) 
