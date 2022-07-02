import datetime
from src.entities.booking import Booking
from src.infrastructure import bookings_repository, bookings_scheduler_repository
from src.infrastructure.bookings_repository import ExceededBookingLimitException, CanNotBookAtTheSameTimeException, NotAllowedForThisClassException, ExceededDailyBookingLimitException, PendingPaymentException 

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


async def remove_user_scheduled_booking(was_booking_scheduled: bool, booking: Booking, mail: str) -> Booking:
    if was_booking_scheduled:
        await bookings_scheduler_repository.remove_user_scheduled_booking(booking=booking, mail=mail)
    


async def make_booking(booking: Booking, mail: str) -> Booking:
    was_booking_scheduled = booking.is_scheduled()

    # Discard booking if class already started
    if booking.has_started():
        await remove_user_scheduled_booking(was_booking_scheduled, booking, mail)
        raise ClassAlreadyStartedException("This class has already started")

    # Some classes might be disabled (canceled) but you can still book them
    if not booking.enabled:
        await remove_user_scheduled_booking(was_booking_scheduled, booking, mail)
        raise NotAllowedForThisClassException("This class is not allowed for booking")

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
                PendingPaymentException,
                ExceededBookingLimitException, 
                CanNotBookAtTheSameTimeException):
            booking.status = "CANCELED"
            print(f'Discarding booking {booking.id} at {booking.start_timestamp}')
            pass
        
        await remove_user_scheduled_booking(was_booking_scheduled, booking, mail)
        
    # Class can be booked but is full. Schedule it if it wasn't already
    elif booking.is_in_range_to_book() and booking.is_full() and (not was_booking_scheduled):
        
        # Remove first the scheduled class if it was
        await remove_user_scheduled_booking(was_booking_scheduled, booking, mail)

        booking = await bookings_scheduler_repository.schedule_booking(
            booking=booking,
            booking_date=datetime.datetime.now() + datetime.timedelta(seconds=60 * 2),
            mail=mail,
        )

    # Schedule booking if it wasn't already
    elif (booking.status == "NONE") and (not was_booking_scheduled):
        booking = await bookings_scheduler_repository.schedule_booking(
            booking=booking,
            booking_date=booking.get_next_bookable_date(),
            mail=mail,
        )

    return booking


async def make_booking_by_id(booking_id: str, date: datetime.datetime, mail: str) -> Booking:

    # Find booking
    booking = await bookings_repository.get_booking_by_id(
        day=date, booking_id=booking_id, mail=mail
    )
    if not booking:
        # Scheduled class might have been deleted from aimharder 
        await bookings_scheduler_repository.remove_user_scheduled_booking_by_id_and_date(booking_id, date, mail)

        raise BookingDoesNotExistException(
            f"Booking {booking_id} on date {date} does not exist"
        )

    return await make_booking(booking=booking, mail=mail)