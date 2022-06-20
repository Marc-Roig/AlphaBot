from src.entities.booking import Booking
from src.infrastructure import bookings_repository, bookings_scheduler_repository


async def list_booked_classes(
    mail: str
) -> list[Booking]:

    bookings = await bookings_repository.get_next_bookings(mail=mail)
    scheduled_bookings = await bookings_scheduler_repository.get_user_scheduled_bookings(mail=mail)
    
    return [*bookings, *scheduled_bookings]
