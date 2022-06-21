import datetime
from src.entities.booking import Booking
from src.infrastructure import bookings_repository, bookings_scheduler_repository
from src.infrastructure.bookings_repository import ExceededBookingLimitException, CanNotBookAtTheSameTimeException, NotAllowedForThisClassException, ExceededDailyBookingLimitException 

class BookingDoesNotExistException(Exception):
    """
    Raised when looking for a booking that does not exist
    """
    def __init__(self, message, errors = []):            
        super().__init__(message)
        self.errors = errors


class AlreadyBookedException(Exception):
    """
    Raised when trying to book an already booked class
    """
    def __init__(self, message, errors = []):            
        super().__init__(message)
        self.errors = errors


class ClassAlreadyStartedException(Exception):
    """
    Raised when trying to book an already booked class
    """
    def __init__(self, message, errors = []):            
        super().__init__(message)
        self.errors = errors


async def make_booking(booking_id: str, date: datetime.datetime, mail: str) -> Booking:

    # Find booking
    booking = await bookings_repository.get_booking_by_id(
        day=date, booking_id=booking_id, mail=mail
    )
    if not booking:
        raise BookingDoesNotExistException(
            f"Booking {booking_id} on date {date} does not exist"
        )

    # TODO: Manage retries
    was_booking_scheduled = booking.is_scheduled()

    if booking.has_started():
        raise ClassAlreadyStartedException("This class has already started")

    # If it is already booked
    if booking.is_booked():
        raise AlreadyBookedException("This class is already booked")
    
    # Check if its in range to book
    elif booking.is_bookable():

        try:
            booking = await bookings_repository.book(booking=booking, mail=mail)
        # If user is not allowed to book for that time, continue and discard this booking
        except (ExceededDailyBookingLimitException,
                NotAllowedForThisClassException, 
                ExceededBookingLimitException, 
                CanNotBookAtTheSameTimeException):
            booking.status = "CANCELED"
            print(f'Discarding booking {booking_id} at {date}')
            pass

        if was_booking_scheduled:
            await bookings_scheduler_repository.remove_user_scheduled_booking(booking=booking, mail=mail)

    # Class can be booked but is full
    elif booking.is_in_range_to_book() and booking.is_full() and not was_booking_scheduled:
        
        # Remove first the scheduled class if it was
        if was_booking_scheduled:
            await bookings_scheduler_repository.remove_user_scheduled_booking(booking=booking, mail=mail)

        booking = await bookings_scheduler_repository.schedule_booking(
            booking=booking,
            booking_date=datetime.datetime.now() + datetime.timedelta(seconds=60 * 2),
            mail=mail,
        )

    # Schedule booking
    elif (booking.status == "NONE") and (not was_booking_scheduled):
        booking = await bookings_scheduler_repository.schedule_booking(
            booking=booking,
            booking_date=booking.get_next_bookable_date(),
            mail=mail,
        )

    return booking
