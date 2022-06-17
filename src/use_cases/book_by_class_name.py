import datetime
from src.entities.booking import Booking
from src.infrastructure import bookings_repository, bookings_scheduler_repository


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


async def make_booking(class_name: str, date: datetime.datetime, mail: str) -> Booking:

    # Find booking
    booking = await bookings_repository.get_booking_by_date_and_name(
        date=date, class_type=class_name, mail=mail
    )
    if not booking:
        raise BookingDoesNotExistException(
            f"Booking {class_name} on date {date} does not exist"
        )

    # If it is already booked
    if booking.is_booked():
        raise AlreadyBookedException()

    # Check if its in range to book
    elif booking.is_bookable():
        booking = await bookings_repository.book(booking=booking, mail=mail)

    # Class can be booked but is full
    elif booking.is_in_range_to_book() and booking.is_full():
        booking = await bookings_scheduler_repository.schedule_booking(
            booking=booking,
            booking_date=datetime.datetime.now() + datetime.timedelta(seconds=60 * 2),
            mail=mail,
        )

    # Schedule booking
    elif booking.status == "NONE":
        booking = await bookings_scheduler_repository.schedule_booking(
            booking=booking,
            booking_date=booking.get_next_bookable_date()
            + datetime.timedelta(seconds=1),
            mail=mail,
        )

    return booking
