from .bookings_repository import BookingsRepository
from .schedule_bookings_repository import BookingsSchedulerRepository
from .user_access_repository import UserAccessRepository

user_access_repository = UserAccessRepository()
bookings_scheduler_repository = BookingsSchedulerRepository()
bookings_repository = BookingsRepository(
    user_access_repository=user_access_repository,
    scheduled_booking_repository=bookings_scheduler_repository,
)

