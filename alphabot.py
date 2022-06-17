import datetime
from telegram.ext import Application
from src.commands import add_user_commands, add_repeating_jobs

from src.infrastructure import bookings_repository, bookings_scheduler_repository
import asyncio

TOKEN = "5449340591:AAGQ05hp2NliXxz9zowlWVLUg-vZ-LsGeIM"

async def _schedule_test():
        # Find booking
    booking = await bookings_repository.get_booking_by_date_and_name(
        date=datetime.datetime(2022, 6, 14, 13), class_type="FITCOND", mail="marc12info@gmail.com"
    )
        
    booking = await bookings_scheduler_repository.schedule_booking(
        booking=booking,
        booking_date=datetime.datetime.now() + datetime.timedelta(seconds=60 * 2),
        mail="marc12info@gmail.com",
    )


def main() -> None:
        
    # loop = asyncio.new_event_loop()
    # loop.run_until_complete(_schedule_test())

    # Initialize the bot
    telegram_app = Application.builder().token(TOKEN).build()

    # Add handlers
    add_user_commands(telegram_app)
    add_repeating_jobs(telegram_app)

    # Run the bot
    telegram_app.run_polling()


if __name__ == "__main__":
    main()
