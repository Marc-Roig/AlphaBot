from src.infrastructure import start_beanie
from src.infrastructure.user_mongo_repository import CredentialsError, UserMongoRepository, Users
import asyncio
import pytest
import os

@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()

@pytest.fixture(scope="module")
async def client():
    os.environ['MONGO_DB'] = 'test'
    await start_beanie()
    yield

    # await Users.delete_all()



user_access_repository = UserMongoRepository()

async def test_login_valid(client: None) -> None:
    cookie = await user_access_repository.login(
        "marc12info@gmail.com", os.environ["AIM_PASSWORD"]
    )
    assert cookie

async def test_login_invalid(client: None) -> None:
    with pytest.raises(CredentialsError):
        await user_access_repository.login("marc12info@gmail.com", "1234")
