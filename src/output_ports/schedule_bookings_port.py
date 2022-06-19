from typing import Optional, Protocol, Literal
from http.cookiejar import Cookie as HttpCookie, CookieJar
from pydantic import BaseModel
from datetime import datetime

from src.entities.booking import Booking


class BookingAlreadyScheduledException(Exception):
    pass


class ScheduledBooking(BaseModel):
    date: datetime
    booking: Booking
    mail: str


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