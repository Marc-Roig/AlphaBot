"""
Cron to book scheduled classes.
"""
from telegram.ext import CallbackContext
from src.use_cases.book_user_scheduled_classes import make_bookings
import asyncio

import datetime
async def handler(context: CallbackContext) -> None:
    
    users = ["marc12info@gmail.com"]
    bookings_promises = []

    for user in users:
        
        bookings_promises.extend(
            await make_bookings(user)
        )

    await asyncio.gather(*bookings_promises)