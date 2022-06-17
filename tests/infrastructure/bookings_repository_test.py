from src.infrastructure.bookings_repository import BookingsRepository
from src.infrastructure.user_repository import UserRepository
from src.infrastructure.schedule_bookings_repository import BookingsSchedulerRepository
from datetime import datetime
import pytest


user_access_repository = UserRepository()
bookings_scheduler_repository = BookingsSchedulerRepository()
bookings_repository = BookingsRepository(
    user_access_repository=user_access_repository,
    scheduled_booking_repository=bookings_scheduler_repository,
)


@pytest.mark.asyncio
async def test_get_daily_bookings() -> None:
    bookings = await bookings_repository.get_daily_bookings(
        day=datetime.strptime("06/06/2022", "%d/%m/%Y"), mail="marc12info@gmail.com"
    )

    assert len(bookings) == 8
    assert bookings[2].status == "BOOKED"


@pytest.mark.asyncio
async def test_get_daily_bookings_with_invalid_mail() -> None:

    with pytest.raises(Exception):
        bookings = await bookings_repository.get_daily_bookings(
            day=datetime.strptime("06/06/2022", "%d/%m/%Y"), mail="wrong@gmail.com"
        )


@pytest.mark.asyncio
async def test_get_booking_by_date_and_name() -> None:

    booking = await bookings_repository.get_booking_by_date_and_name(
        date=datetime.strptime("06/06/2022 10:00:00", "%d/%m/%Y %H:%M:%S"),
        class_type="WOD WEEK-END",
        mail="marc12info@gmail.com",
    )

    assert booking


@pytest.mark.asyncio
async def test_get_scheduled_booking() -> None:

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


@pytest.mark.asyncio
async def _test_booking() -> None:

    booking = await bookings_repository.get_booking_by_date_and_name(
        date=datetime.strptime("09/06/2022 11:00:00", "%d/%m/%Y %H:%M:%S"),
        class_type="WOD",
        mail="marc12info@gmail.com",
    )

    booking = await bookings_repository.book(booking, mail="marc12info@gmail.com")

    assert booking.is_booked()


@pytest.mark.asyncio
async def _test_cancel_booking() -> None:

    booking = await bookings_repository.get_booking_by_date_and_name(
        date=datetime.strptime("09/06/2022 11:00:00", "%d/%m/%Y %H:%M:%S"),
        class_type="WOD",
        mail="marc12info@gmail.com",
    )

    booking = await bookings_repository.cancel_booking(
        booking, mail="marc12info@gmail.com"
    )

    assert not booking.is_booked()
