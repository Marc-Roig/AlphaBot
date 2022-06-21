import datetime
from src.entities.booking import Booking
from src.infrastructure import bookings_repository, bookings_scheduler_repository


class BookingDoesNotExistException(Exception):
    """
    Raised when looking for a booking that does not exist
    """
    pass


class NotBookedException(Exception):
    """
    Raised when trying to cancel a class that is not booked
    """
    pass


async def cancel_booking(class_name: str, date: datetime.datetime, mail: str) -> Booking:

    print("Canceling booking for", class_name, date, mail)
    # Find booking
    booking = await bookings_repository.get_booking_by_date_and_name(
        date=date, class_type=class_name, mail=mail
    )
    if not booking:
        raise BookingDoesNotExistException(
            f"Booking {class_name} on date {date} does not exist"
        )

    if booking.is_booked():
        booking = await bookings_repository.cancel_booking(booking=booking, mail=mail)

    elif booking.is_scheduled():
        booking = await bookings_scheduler_repository.remove_user_scheduled_booking(
            booking=booking, mail=mail
        )
    else:
        raise NotBookedException()

    booking.status = "CANCELED"

    return booking