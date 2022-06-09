from src.infrastructure.user_access_repository import (
    CredentialsError,
    UserAccessRepository,
)
import pytest
import os

user_access_repository = UserAccessRepository()


class TestUserAccessRepository:
    @pytest.mark.asyncio
    async def test_cookies_initialized(self) -> None:
        assert await user_access_repository.get_cookies("marc12info@gmail.com")

    @pytest.mark.asyncio
    async def test_login_valid(self) -> None:
        cookie = await user_access_repository.login(
            "marc12info@gmail.com", os.environ["AIM_PASSWORD"]
        )
        assert cookie

    @pytest.mark.asyncio
    async def test_login_invalid(self) -> None:
        with pytest.raises(CredentialsError):
            await user_access_repository.login("marc12info@gmail.com", "1234")
