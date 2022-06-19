from datetime import datetime
from src.entities.booking import Booking
from src.output_ports.schedule_bookings_port import BookingAlreadyScheduledException, BookingsSchedulerPort, ScheduledBooking
from beanie import Document

class ScheduledBookings(Document):
    date: datetime
    booking: Booking
    mail: str
    retries: int = 0

def db_to_domain(scheduled_booking_db: ScheduledBookings) -> ScheduledBooking:
    return ScheduledBooking(
        date=scheduled_booking_db.date,
        booking=scheduled_booking_db.booking,
        mail=scheduled_booking_db.mail,
    )

def domain_to_db(scheduled_booking: ScheduledBooking) -> ScheduledBookings:
    return ScheduledBookings(
        date=scheduled_booking.date,
        booking=scheduled_booking.booking,
        mail=scheduled_booking.mail,
    )


class BookingsSchedulerMongoRepository(BookingsSchedulerPort):

    async def is_booking_scheduled(self, booking: Booking, mail: str) -> bool:

        booking = await ScheduledBookings.find_one({"mail": mail, "booking.id": booking.id})
        if booking:
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

        scheduled_booking_db = domain_to_db(ScheduledBooking(date=booking_date, booking=booking, mail=mail))
        await scheduled_booking_db.create()

        return booking

    async def get_user_scheduled_bookings(self, mail: str) -> list[Booking]:

        scheduled_bookings_db = await ScheduledBookings.find({"mail": mail}).to_list()
        return [db_to_domain(scheduled_booking).booking for scheduled_booking in scheduled_bookings_db]


    async def get_user_scheduled_bookings_from_date(
        self, mail: str, date: datetime
    ) -> list[Booking]:
        scheduled_bookings_db = await ScheduledBookings.find({"mail": mail, "date": {"$lte": date}}).to_list()
        return [db_to_domain(scheduled_booking).booking for scheduled_booking in scheduled_bookings_db]

    async def remove_user_scheduled_booking(
        self, booking: Booking, mail: str
    ) -> Booking:

        await ScheduledBookings.find_many({"mail": mail, "booking.id": booking.id}).delete()

        if booking.status == "SCHEDULED":
            booking.status = "NONE"

        return booking
