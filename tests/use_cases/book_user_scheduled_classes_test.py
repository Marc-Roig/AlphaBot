
import asyncio
from src.entities.booking import Booking
from src.infrastructure.bookings_repository import BookingsRepository
from src.infrastructure.schedule_bookings_repository import BookingsSchedulerRepository
from src.infrastructure.user_repository import UserRepository
from src.infrastructure import bookings_scheduler_repository
import datetime
import pytest

from src.use_cases.book_user_scheduled_classes import make_bookings

user_access_repository = UserRepository()
bookings_repository = BookingsRepository(
    user_access_repository=user_access_repository,
    scheduled_booking_repository=bookings_scheduler_repository,
)

@pytest.fixture()
async def schedule_class():
    
    booking = await bookings_repository.get_booking_by_date_and_name(
        date=datetime.datetime(2022, 6, 14, 13), class_type="FITCOND", mail="marc12info@gmail.com"
    )
        
    booking = await bookings_scheduler_repository.schedule_booking(
        booking=booking,
        booking_date=datetime.datetime.now() - datetime.timedelta(seconds=10),
        mail="marc12info@gmail.com",
    )

    yield booking

    await bookings_scheduler_repository.remove_user_scheduled_booking(booking, "marc12info@gmail.com")

async def test_bookable_scheduled_class(schedule_class: Booking) -> None:
    """
    Test that bookable scheduled class is booked.
    """

    bookings_promises = await make_bookings(
        mail="marc12info@gmail.com",
    )

    results: list[Booking] = await asyncio.gather(*bookings_promises)

    assert len(results) == 1
    assert results[0].status == "BOOKED"
