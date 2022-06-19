from src.infrastructure.bookings_repository import BookingsRepository
from src.infrastructure.user_mongo_repository import UserMongoRepository
from src.infrastructure.schedule_bookings_mongo_repository import BookingsSchedulerMongoRepository
from src.infrastructure import start_beanie

from datetime import datetime
import pytest
import asyncio
import os

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



async def test_get_daily_bookings(client: None) -> None:
    bookings = await bookings_repository.get_daily_bookings(
        day=datetime.strptime("06/06/2022", "%d/%m/%Y"), mail="marc12info@gmail.com"
    )

    assert len(bookings) == 8
    assert bookings[2].status == "BOOKED"


async def test_get_daily_bookings_with_invalid_mail(client: None) -> None:

    with pytest.raises(Exception):
        bookings = await bookings_repository.get_daily_bookings(
            day=datetime.strptime("06/06/2022", "%d/%m/%Y"), mail="wrong@gmail.com"
        )


async def test_get_booking_by_date_and_name(client: None) -> None:

    booking = await bookings_repository.get_booking_by_date_and_name(
        date=datetime.strptime("06/06/2022 10:00:00", "%d/%m/%Y %H:%M:%S"),
        class_type="WOD WEEK-END",
        mail="marc12info@gmail.com",
    )

    assert booking


async def test_get_next_bookings(client: None) -> None:

    # Make sure there is at least one booking in the future
    bookings = await bookings_repository.get_next_bookings("marc12info@gmail.com")

    assert len(bookings) > 0


async def test_get_scheduled_booking(client: None) -> None:

    # Get a booking
    booking = await bookings_repository.get_booking_by_date_and_name(
        date=datetime.strptime("06/06/2022 10:00:00", "%d/%m/%Y %H:%M:%S"),
        class_type="WOD WEEK-END",
        mail="marc12info@gmail.com",
    )

    # Schedule booking and check its status when getting it
    await bookings_scheduler_repository.schedule_booking(
        booking, datetime(2022, 1, 1, 10, 0), "marc12info@gmail.com"
    )

    booking = await bookings_repository.get_booking_by_date_and_name(
        date=datetime.strptime("06/06/2022 10:00:00", "%d/%m/%Y %H:%M:%S"),
        class_type="WOD WEEK-END",
        mail="marc12info@gmail.com",
    )

    assert booking
    assert booking.status == "SCHEDULED"


async def _test_booking(client: None) -> None:

    booking = await bookings_repository.get_booking_by_date_and_name(
        date=datetime.strptime("09/06/2022 11:00:00", "%d/%m/%Y %H:%M:%S"),
        class_type="WOD",
        mail="marc12info@gmail.com",
    )

    booking = await bookings_repository.book(booking, mail="marc12info@gmail.com")

    assert booking.is_booked()


async def _test_cancel_booking(client: None) -> None:

    booking = await bookings_repository.get_booking_by_date_and_name(
        date=datetime.strptime("09/06/2022 11:00:00", "%d/%m/%Y %H:%M:%S"),
        class_type="WOD",
        mail="marc12info@gmail.com",
    )

    booking = await bookings_repository.cancel_booking(
        booking, mail="marc12info@gmail.com"
    )

    assert not booking.is_booked()
