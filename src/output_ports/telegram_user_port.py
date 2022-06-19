from typing import Optional, Protocol, Literal
from http.cookiejar import Cookie as HttpCookie, CookieJar
from pydantic import BaseModel

class UserAlreadyExistsException(Exception):
    pass

class TelegramUser(BaseModel):
    id: str
    email: str
    username: str
    role: Literal["ADMIN", "USER"] = "USER"


class TelegramUserPort(Protocol):

    async def add_user(self, user: TelegramUser) -> None:
        pass

    async def remove_user(self, telegram_id: str) -> None:
        pass

    async def get_user_by_telegram_id(self, telegram_id: str) -> Optional[TelegramUser]:
        pass

    async def get_all_user_ids(self) -> list[str]:
        pass

    async def get_all_admin_ids(self) -> list[str]:
        pass