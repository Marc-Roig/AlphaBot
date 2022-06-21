import datetime
import logging
from typing import Awaitable

from src.use_cases.book import make_booking
from src.entities.booking import Booking
from src.infrastructure import bookings_scheduler_repository


logger = logging.getLogger("book_user_scheduled_classes")


class BookingDoesNotExistException(Exception):
    """
    Raised when looking for a booking that does not exist
    """

    pass


class AlreadyBookedException(Exception):
    """
    Raised when trying to book an already booked class
    """

    pass

async def _make_booking(booking_id: int, start_timestamp: datetime.datetime, mail: str) -> Booking:
    try:
        logger.info(f"Trying to book {booking_id} at {start_timestamp} for {mail}. Time {datetime.datetime.now()}") 
        booking = await make_booking(booking_id, start_timestamp, mail)
        return booking
    except Exception as e:
        logger.error(e)
    return None

async def make_bookings(mail: str) -> list[Awaitable[Booking]]:

    bookings = await bookings_scheduler_repository.get_user_scheduled_bookings_from_date(
        mail=mail,
        date=datetime.datetime.now()
    )
    
    bookings_promises: list[Awaitable] = []

    for booking in bookings:
        bookings_promises.append(
            _make_booking(booking.id, booking.start_timestamp, mail)
        )

    return bookings_promises