from src.infrastructure.telegram_user_mongo_repository import TelegramUserMongoRepository, TelegramUser, UserAlreadyExistsException
from src.infrastructure import start_beanie
import asyncio
import pytest
import os

telegram_user_repository = TelegramUserMongoRepository()

@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()

@pytest.fixture(scope="module")
async def client():
    os.environ['MONGO_DB'] = 'test'
    await start_beanie()

@pytest.fixture(scope="module")
async def telegram_user(client):

    user = TelegramUser(id="000", email="test@gmail.com", username="test", role="ADMIN")
    await telegram_user_repository.add_user(user)

    try:
        yield user
    finally:
        await telegram_user_repository.remove_user(user.id)

@pytest.fixture(scope="module")
async def telegram_user2(client):

    user = TelegramUser(id="001", email="test2@gmail.com", username="test", role="USER")
    await telegram_user_repository.add_user(user)

    try:
        yield user
    finally:
        await telegram_user_repository.remove_user(user.id)


async def test_get_user_by_telegram_id(telegram_user):
    user = await telegram_user_repository.get_user_by_telegram_id(telegram_user.id)
    assert user == telegram_user

async def test_create_user_already_in_db(telegram_user):
    with pytest.raises(UserAlreadyExistsException):
        user = TelegramUser(id="000", email="test2@gmail.com", username="test2", role="USER")
        await telegram_user_repository.add_user(user)

async def test_get_all_user_ids(telegram_user, telegram_user2):
    user_ids = await telegram_user_repository.get_all_user_ids()
    assert len(user_ids) == 2 
    assert user_ids[0] == "000"
    assert user_ids[1] == "001"

async def test_get_all_admin_ids(telegram_user, telegram_user2):
    admin_ids = await telegram_user_repository.get_all_admin_ids()
    assert len(admin_ids) == 1