
import asyncio
from src.entities.booking import Booking
from src.infrastructure.bookings_repository import BookingsRepository
from src.infrastructure.schedule_bookings_mongo_repository import BookingsSchedulerMongoRepository
from src.infrastructure.user_mongo_repository import UserMongoRepository
from src.infrastructure import start_beanie
import datetime
import pytest
import os

from src.use_cases.book_user_scheduled_classes import make_bookings

user_access_repository = UserMongoRepository()
bookings_scheduler_repository = BookingsSchedulerMongoRepository()
bookings_repository = BookingsRepository(
    user_access_repository=user_access_repository,
    scheduled_booking_repository=bookings_scheduler_repository,
)

@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()

@pytest.fixture(scope="module")
async def client():
    os.environ['MONGO_DB'] = 'test'
    await start_beanie()

@pytest.fixture()
async def schedule_class(client):
    
    booking = await bookings_repository.get_booking_by_date_and_name(
        date=datetime.datetime(2022, 6, 19, 12), class_type="WOD WEEK-END", mail="marc12info@gmail.com"
    )
        
    booking = await bookings_scheduler_repository.schedule_booking(
        booking=booking,
        booking_date=datetime.datetime.now() - datetime.timedelta(seconds=10),
        mail="marc12info@gmail.com",
    )
    try:
        yield booking
    finally:
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
