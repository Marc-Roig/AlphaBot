from .bookings_repository import BookingsRepository
from .schedule_bookings_repository import BookingsSchedulerRepository
from .user_repository import UserRepository
from .telegram_user_repository import TelegramUserRepository

user_repository = UserRepository()
telegram_user_repository = TelegramUserRepository()
bookings_scheduler_repository = BookingsSchedulerRepository()
bookings_repository = BookingsRepository(
    user_access_repository=user_repository,
    scheduled_booking_repository=bookings_scheduler_repository,
)

