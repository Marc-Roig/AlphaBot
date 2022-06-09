from typing import Any, Optional
from httpx import AsyncClient
import datetime
import asyncio
import re
import os

from src.entities.booking import Booking
from src.infrastructure.user_access_repository import UserAccessRepository
from src.infrastructure.schedule_bookings_repository import BookingsSchedulerRepository


# TODO: Errors file
class CouldNotGetBookingsException(Exception):
    pass


class FullClassException(Exception):
    pass


class NotAllowedForThisClassException(Exception):
    pass


class ExceededBookingLimitException(Exception):
    pass


class ExceededDailyBookingLimitException(Exception):
    pass


class CanNotBookAtTheSameTimeException(Exception):
    pass


class CanNotBookInAdvanceException(Exception):
    pass


class CanNotCancelBookingException(Exception):
    pass


# TODO: Constants file
book_state = {"0": "QUEUED", "1": "BOOKED", 0: "QUEUED", 1: "BOOKED", None: "NONE"}


def get_wait_list_occupation(limit):
    res = re.findall(r"\((.*?)\)", limit)
    if len(res):
        return int(res[0])
    return 0


async def alpha_booking_to_domain(
    scheduled_booking_repository: BookingsSchedulerRepository,
    alpha_booking: Any,
    date: datetime.datetime,
    mail: str,
) -> Booking:

    # Alpha only returns booking time as `HH:MM - HH:MM` (start - end).
    # Parse it to store it as start_timestamp / end_timestamp
    start, end = alpha_booking["time"].split(" - ")

    start = datetime.datetime.strptime(start, "%H:%M")
    end = datetime.datetime.strptime(end, "%H:%M")

    _date = date.replace(hour=0, minute=0, second=0, microsecond=0)

    start_timestamp = _date + datetime.timedelta(hours=start.hour, minutes=end.minute)
    end_timestamp = _date + datetime.timedelta(hours=end.hour, minutes=end.minute)

    booking = Booking(
        status=book_state[alpha_booking["bookState"]],
        id=alpha_booking["id"],
        enabled=alpha_booking["enabled"],
        cancel_id=alpha_booking["idres"],
        occupation=alpha_booking["ocupation"],
        class_name=alpha_booking["className"],
        wait_list_occupation=get_wait_list_occupation(alpha_booking["limit"]),
        limit=alpha_booking["limitc"],
        start_timestamp=start_timestamp,
        end_timestamp=end_timestamp,
    )

    # Check if booking is scheduled and override status value if it is
    is_booking_scheduled = await scheduled_booking_repository.is_booking_scheduled(
        booking=booking, mail=mail
    )
    if is_booking_scheduled:
        booking.status = "SCHEDULED"

    return booking


_client = AsyncClient()


class BookingsRepository:
    def __init__(
        self,
        user_access_repository: UserAccessRepository,
        scheduled_booking_repository: BookingsSchedulerRepository,
    ):
        self.user_access_repository = user_access_repository
        self.scheduled_booking_repository = scheduled_booking_repository

    async def get_daily_bookings(
        self, day: datetime.datetime, mail: str
    ) -> list[Booking]:

        try:

            # Get session cookies
            cookies = await self.user_access_repository.get_cookies(mail)

            if not cookies:
                raise Exception("Not Logged In")

            # Find booking
            response = await _client.get(
                "https://alphalinkcrossfit.aimharder.com/api/bookings",
                params={
                    "day": day.strftime("%Y%m%d"),
                    "familyId": "",
                    "box": os.environ["BOD_ID"],
                },
                cookies=cookies,
                follow_redirects=True,
            )

            bookings: list[Booking] = await asyncio.gather(
                *[
                    alpha_booking_to_domain(
                        scheduled_booking_repository=self.scheduled_booking_repository,
                        alpha_booking=booking,
                        date=day,
                        mail=mail,
                    )
                    for booking in response.json()["bookings"]
                ]
            )

        except Exception as e:
            # TODO: Log error
            raise CouldNotGetBookingsException(
                f"Could not get bookings for {day}. \n Error: {e}"
            )

        return bookings

    # TODO: class type to enum
    async def get_booking_by_date_and_name(
        self, date: datetime.datetime, class_type: str, mail: str
    ) -> Optional[Booking]:

        bookings = await self.get_daily_bookings(day=date, mail=mail)

        for booking in bookings:
            if (booking.class_name == class_type) and (
                booking.start_timestamp == date.replace(second=0)
            ):
                return booking

        return None

    async def get_booking_by_id(
        self, day: datetime.datetime, booking_id: str, mail: str
    ) -> Optional[Booking]:

        bookings = await self.get_daily_bookings(day=day, mail=mail)

        for booking in bookings:
            if booking.id == booking_id:
                return booking

        return None

    async def book(self, booking: Booking, mail: str) -> Booking:

        # Get session cookies
        cookies = await self.user_access_repository.get_cookies(mail)

        # Book class
        response = await _client.post(
            "https://alphalinkcrossfit.aimharder.com/api/book",
            data={
                "id": booking.id,
                "day": booking.start_timestamp.strftime("%Y%m%d"),
                "insist": 0,
                "familiId": "",
            },
            cookies=cookies,
            follow_redirects=True,
        )
        # TODO: IF -8, Error Can not make more than 1 reservation per day

        if (response.status_code == 200) and ("bookState" in response.json()):

            state = response.json()["bookState"]

            if state == 0:
                # TODO: Update cancel id and booking status
                # booking.cancel_id = res_dict['id'] #TODO
                booking.status = "QUEUED"
                booking.cancel_id = response.json()["id"]
                return booking

            elif state == 1:
                booking.status = "BOOKED"
                booking.cancel_id = response.json()["id"]
                return booking

            elif state == -1:
                raise FullClassException()

            elif state == -2:
                raise NotAllowedForThisClassException()

            elif state == -8:
                raise ExceededDailyBookingLimitException()

            elif state == -12:

                error_key = response.json().get("errorMssgLang", "")

                if error_key == "HASSUPERADOLIMITCONTR":
                    raise ExceededBookingLimitException()
                elif error_key == "NOPUEDESRESERVAMISMAHORA":
                    raise CanNotBookAtTheSameTimeException()
                elif error_key == "ERROR_ANTELACION_CLIENTE":
                    raise CanNotBookInAdvanceException()

        # TODO: Manage errors
        raise Exception("Could not make booking")

    async def cancel_booking(self, booking: Booking, mail: str) -> Booking:

        # Get session cookies
        cookies = await self.user_access_repository.get_cookies(mail)

        # Cancel booking
        response = await _client.post(
            "https://alphalinkcrossfit.aimharder.com/api/cancelBook",
            data={"id": booking.cancel_id, "late": 0, "familiId": ""},
            cookies=cookies,
            follow_redirects=True,
        )

        # Check if canceled
        if (response.status_code == 200) and ("cancelState" in response.json()):
            booking.status = "NONE"
            return booking

        # TODO: Custom error
        raise CanNotCancelBookingException("Could not cancel booking")

