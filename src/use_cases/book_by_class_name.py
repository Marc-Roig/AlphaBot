import datetime
from src.entities.booking import Booking
from src.infrastructure import bookings_repository
from src.use_cases.book import (
    make_booking, 
    BookingDoesNotExistException, 
    AlreadyBookedException, 
    ClassAlreadyStartedException
)


async def make_booking_by_name(class_name: str, date: datetime.datetime, mail: str) -> Booking:

    # Find booking
    booking = await bookings_repository.get_booking_by_date_and_name(
        date=date, class_type=class_name, mail=mail
    )
    if not booking:
        raise BookingDoesNotExistException(
            f"Booking {class_name} on date {date} does not exist"
        )

    return await make_booking(booking=booking, mail=mail)