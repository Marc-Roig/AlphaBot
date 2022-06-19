from src.entities.booking import Booking
from src.infrastructure import start_beanie
from src.infrastructure.bookings_repository import BookingsRepository
from src.infrastructure.schedule_bookings_mongo_repository import BookingsSchedulerMongoRepository
from src.infrastructure.user_mongo_repository import UserMongoRepository
from datetime import datetime
import pytest
import asyncio
import os

from src.use_cases.book import make_booking

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


async def test_make_booking(client: None) -> None:
    """"
    Test that a simple booking can be made.
    """

    bookable_class = await bookings_repository.get_booking_by_date_and_name(
        datetime(2022, 6, 21, 11, 0, 0),  # This day was monday
        "WOD",
        "marc12info@gmail.com",
    )

    assert bookable_class

    bookable_class = await make_booking(
        booking_id=bookable_class.id,
        date=bookable_class.start_timestamp,
        mail="marc12info@gmail.com",
    )

    assert bookable_class.status == "BOOKED"
    await bookings_repository.cancel_booking(bookable_class, "marc12info@gmail.com")

async def test_schedule_full_booking(client: None) -> None:
    """
    Test that a booking can be scheduled when the class is full
    """

    scheduled_class = await bookings_repository.get_booking_by_date_and_name(
        datetime(2022, 6, 19, 11, 0, 0),  # This day was monday
        "FITCOND WEEK-END",
        "marc12info@gmail.com",
    )

    assert scheduled_class

    scheduled_class = await make_booking(
        booking_id=scheduled_class.id,
        date=scheduled_class.start_timestamp,
        mail="marc12info@gmail.com"
    )

    assert scheduled_class.status == "SCHEDULED"

async def test_schedule_future_booking() -> None:
    """
    Test that a booking can be scheduled in the future.
    When is not 4 days from today.
    """

    scheduled_class = await bookings_repository.get_booking_by_date_and_name(
        datetime(2022, 6, 18, 13, 0, 0),  # This day was monday
        "OPEN BOX WEEKEND",
        "marc12info@gmail.com",
    )

    assert scheduled_class

    scheduled_class = await make_booking(
        booking_id=scheduled_class.id,
        date=scheduled_class.start_timestamp,
        mail="marc12info@gmail.com"
    )

    assert scheduled_class.status == "SCHEDULED"