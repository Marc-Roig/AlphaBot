from src.infrastructure import start_beanie
from src.infrastructure.schedule_bookings_mongo_repository import (
    BookingAlreadyScheduledException,
    BookingsSchedulerMongoRepository,
    ScheduledBookings
)
from src.entities.booking import Booking
from datetime import datetime
import pytest
import asyncio
import os


booking = Booking(
    status="NONE",
    id="1234",
    class_name="WOD",
    enabled=True,
    cancel_id="1234",
    occupation=0,
    limit=20,
    wait_list_occupation=0,
    start_timestamp=datetime(2020, 1, 1, 10, 0),
    end_timestamp=datetime(2020, 1, 1, 11, 0),
)

bookings_scheduler_repository = BookingsSchedulerMongoRepository()

@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()

@pytest.fixture(scope="module")
async def client():
    os.environ['MONGO_DB'] = 'test'
    await start_beanie()

@pytest.fixture
async def clean_db(client):
    yield
    await ScheduledBookings.find_all().delete()


async def test_is_booking_scheduled_wrong_booking(
    client: None
) -> None:
    assert not await bookings_scheduler_repository.is_booking_scheduled(
        booking, "mail@gmail.com"
    )


async def test_schedule_booking(
    client: None, clean_db: None,
) -> None:

    await bookings_scheduler_repository.schedule_booking(
        booking, datetime(2020, 1, 1, 10, 0), "mail@gmail.com"
    )

    is_scheduled = await bookings_scheduler_repository.is_booking_scheduled(
        booking, "mail@gmail.com"
    )

    assert booking.status == "SCHEDULED"
    assert is_scheduled


async def test_schedule_booking_twice(
    client: None, clean_db: None,
) -> None:

    await bookings_scheduler_repository.schedule_booking(
        booking, datetime(2020, 1, 1, 10, 0), "mail@gmail.com"
    )

    with pytest.raises(BookingAlreadyScheduledException):
        await bookings_scheduler_repository.schedule_booking(
            booking, datetime(2020, 1, 1, 10, 0), "mail@gmail.com"
        )


async def test_get_user_scheduled_bookings(
    client: None, clean_db: None,
) -> None:

    await bookings_scheduler_repository.schedule_booking(
        booking, datetime(2020, 1, 1, 10, 0), "mail@gmail.com"
    )

    await bookings_scheduler_repository.schedule_booking(
        booking, datetime(2020, 1, 1, 10, 0), "mail2@gmail.com"
    )

    bookings = await bookings_scheduler_repository.get_user_scheduled_bookings(
        "mail@gmail.com"
    )

    assert len(bookings) == 1

async def test_get_user_scheduled_bookings_from_date(
    client: None, clean_db: None,
) -> None:

    await bookings_scheduler_repository.schedule_booking(
        booking, datetime(2020, 1, 1, 10, 0), "mail@gmail.com"
    )

    bookings = await bookings_scheduler_repository.get_user_scheduled_bookings_from_date(
        "mail@gmail.com", datetime(2020, 1, 1, 10, 0)
    )

    assert len(bookings) == 1

    bookings = await bookings_scheduler_repository.get_user_scheduled_bookings_from_date(
        "mail@gmail.com", datetime(2020, 1, 1, 9, 0)
    )

    assert len(bookings) == 0


async def test_remove_booking_from_schedule(
    client: None, clean_db: None,
) -> None:

    await bookings_scheduler_repository.schedule_booking(
        booking, datetime(2020, 1, 1, 10, 0), "mail@gmail.com"
    )

    updated_booking = await bookings_scheduler_repository.remove_user_scheduled_booking(
        booking, "mail@gmail.com"
    )

    is_scheduled = await bookings_scheduler_repository.is_booking_scheduled(
        booking, "mail@gmail.com"
    )

    assert updated_booking.status == "NONE"
    assert not is_scheduled

async def test_remove_wrong_booking_by_id_from_schedule(
    client: None, clean_db: None,
) -> None:
    # Try to remove an non existing booking, it should not return any exception
    await bookings_scheduler_repository.remove_user_scheduled_booking_by_id_and_date(
        "1111", datetime(2020, 1, 1, 10, 0), "marc12info@gmail.com"
    )

