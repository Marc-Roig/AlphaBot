"""
Cron to book scheduled classes.
"""
from telegram.ext import CallbackContext
from src.use_cases.book_user_scheduled_classes import make_bookings
from src.infrastructure import user_repository
import asyncio

async def handler(context: CallbackContext) -> None:
    
    users = await user_repository.get_all()
    bookings_promises = []

    for user in users:
        
        bookings_promises.extend(
            await make_bookings(user)
        )

    await asyncio.gather(*bookings_promises)