import datetime
from src.entities.booking import Booking
from src.infrastructure import bookings_repository


async def list_daily_classes(
    date: datetime.datetime, mail: str, filter_by_name: list[str]
) -> list[Booking]:

    bookings = await bookings_repository.get_daily_bookings(day=date, mail=mail)

    if filter_by_name:
        bookings = [b for b in bookings if b.class_name in filter_by_name]

    return bookings
