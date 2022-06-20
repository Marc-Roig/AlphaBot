from typing import Protocol
from pydantic import BaseModel, Field
from datetime import datetime

from src.entities.booking import Booking


class BookingAlreadyScheduledException(Exception):
    pass


class ScheduledBooking(BaseModel):
    date: datetime
    booking: Booking
    mail: str
    retries: int = 0
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class BookingsSchedulerPort(Protocol):

    async def is_booking_scheduled(self, booking: Booking, mail: str) -> bool:
        pass

    async def schedule_booking(
        self, booking: Booking, booking_date: datetime, mail: str
    ) -> Booking:
        pass

    async def get_user_scheduled_bookings(self, mail: str) -> list[Booking]:
        pass

    async def get_user_scheduled_bookings_from_date(
        self, mail: str, date: datetime
    ) -> list[Booking]:
        pass

    async def remove_user_scheduled_booking(
        self, booking: Booking, mail: str
    ) -> Booking:
        pass