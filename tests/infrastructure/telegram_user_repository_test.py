import pytest
from src.infrastructure.telegram_user_repository import TelegramUserRepository, TelegramUser, UserAlreadyExistsException

telegram_user_repository = TelegramUserRepository()

@pytest.fixture()
async def telegram_user():
    user = TelegramUser(id="000", email="test@gmail.com", username="test", role="USER")
    await telegram_user_repository.add_user(user)
    yield user
    await telegram_user_repository.remove_user(user.id)


async def test_get_user_by_telegram_id(telegram_user):

    user = await telegram_user_repository.get_user_by_telegram_id(telegram_user.id)
    assert user == telegram_user

async def test_create_user_already_in_db(telegram_user):
    with pytest.raises(UserAlreadyExistsException):
        user = TelegramUser(id="000", email="test2@gmail.com", username="test2", role="USER")
        await telegram_user_repository.add_user(user)

async def test_get_all_user_ids(telegram_user):
    user_ids = await telegram_user_repository.get_all_user_ids()
    assert len(user_ids) == 2 # Db is initialized with an admin
    assert user_ids[1] == "000"

async def test_get_all_admin_ids(telegram_user):
    admin_ids = await telegram_user_repository.get_all_admin_ids()
    assert len(admin_ids) == 1