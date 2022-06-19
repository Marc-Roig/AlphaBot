import os

from src.infrastructure.schedule_bookings_mongo_repository import BookingsSchedulerMongoRepository
from src.infrastructure.telegram_user_mongo_repository import TelegramUserMongoRepository
from src.infrastructure.user_mongo_repository import UserMongoRepository

from .bookings_repository import BookingsRepository
from beanie import init_beanie
from dotenv import load_dotenv
import motor

load_dotenv()

# Dependency Injection
user_repository = UserMongoRepository()
bookings_scheduler_repository = BookingsSchedulerMongoRepository()
telegram_user_repository = TelegramUserMongoRepository()
bookings_repository = BookingsRepository(
    user_access_repository=user_repository,
    scheduled_booking_repository=bookings_scheduler_repository,
)


# Beanie DB connection startup
async def start_beanie() -> None:
    
    from .user_mongo_repository import Users
    from .telegram_user_mongo_repository import TelegramUsers
    from .schedule_bookings_mongo_repository import ScheduledBookings

    __beanie_models__ = [Users, TelegramUsers, ScheduledBookings]

    # settings = BeanieSettings(_env_file=env_file) # type: ignore
    client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGO_CONNECTION"])

    await init_beanie(
        database=client[os.environ["MONGO_DB"]], document_models=__beanie_models__ # type: ignore
    )
