from src.infrastructure.schedule_bookings_repository import (
    BookingAlreadyScheduledException,
    BookingsSchedulerRepository,
)
from src.entities.booking import Booking
from datetime import datetime
import pytest


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


@pytest.fixture
def bookings_scheduler_repository():
    return BookingsSchedulerRepository()


@pytest.mark.asyncio
async def test_is_booking_scheduled_wrong_booking(bookings_scheduler_repository):
    assert not await bookings_scheduler_repository.is_booking_scheduled(
        booking, "mail@test.com"
    )


@pytest.mark.asyncio
async def test_schedule_booking(
    bookings_scheduler_repository: BookingsSchedulerRepository,
) -> None:

    await bookings_scheduler_repository.schedule_booking(
        booking, datetime(2020, 1, 1, 10, 0), "mail@gmail.com"
    )

    is_scheduled = await bookings_scheduler_repository.is_booking_scheduled(
        booking, "mail@gmail.com"
    )

    assert booking.status == "SCHEDULED"
    assert is_scheduled


@pytest.mark.asyncio
async def test_schedule_booking_twice(
    bookings_scheduler_repository: BookingsSchedulerRepository,
) -> None:

    await bookings_scheduler_repository.schedule_booking(
        booking, datetime(2020, 1, 1, 10, 0), "mail@gmail.com"
    )

    with pytest.raises(BookingAlreadyScheduledException):
        await bookings_scheduler_repository.schedule_booking(
            booking, datetime(2020, 1, 1, 10, 0), "mail@gmail.com"
        )


@pytest.mark.asyncio
async def test_get_user_scheduled_bookings(
    bookings_scheduler_repository: BookingsSchedulerRepository,
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

@pytest.mark.asyncio
async def test_get_user_scheduled_bookings_from_date(
    bookings_scheduler_repository: BookingsSchedulerRepository,
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



@pytest.mark.asyncio
async def test_remove_booking_from_schedule(
    bookings_scheduler_repository: BookingsSchedulerRepository,
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
