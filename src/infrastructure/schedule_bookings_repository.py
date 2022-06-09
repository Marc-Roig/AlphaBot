from datetime import datetime

from pydantic import BaseModel
from src.entities.booking import Booking


class ScheduledBooking(BaseModel):
    date: datetime
    booking: Booking
    mail: str


class BookingAlreadyScheduledException(Exception):
    pass


class BookingsSchedulerRepository:
    def __init__(self):
        self.pending_bookings: list[ScheduledBooking] = []

    async def is_booking_scheduled(self, booking: Booking, mail: str) -> bool:
        for scheduled_booking in self.pending_bookings:
            if (
                booking.id == scheduled_booking.booking.id
                and mail == scheduled_booking.mail
            ):
                return True
        return False

    async def schedule_booking(
        self, booking: Booking, booking_date: datetime, mail: str
    ) -> Booking:
        if await self.is_booking_scheduled(booking, mail):
            raise BookingAlreadyScheduledException(
                f"Booking {booking.class_name} is already scheduled for {booking.start_timestamp}"
            )

        booking.status = "SCHEDULED"

        self.pending_bookings.append(
            ScheduledBooking(date=booking_date, booking=booking, mail=mail)
        )

        return booking

    async def get_user_scheduled_bookings(self, mail: str) -> list[Booking]:
        return [
            scheduled_booking
            for scheduled_booking in self.pending_bookings
            if mail == scheduled_booking.mail
        ]

    async def get_user_scheduled_bookings_from_date(
        self, mail: str, date: datetime
    ) -> list[Booking]:
        return [
            scheduled_booking.booking
            for scheduled_booking in self.pending_bookings
            if mail == scheduled_booking.mail and scheduled_booking.date <= date
        ]

    async def remove_user_scheduled_booking(
        self, booking: Booking, mail: str
    ) -> Booking:
        self.pending_bookings = [
            scheduled_booking
            for scheduled_booking in self.pending_bookings
            if mail != scheduled_booking.mail
            or booking.id != scheduled_booking.booking.id
        ]

        if booking.status == "SCHEDULED":
            booking.status = "NONE"

        return booking
