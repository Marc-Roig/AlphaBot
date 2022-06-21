from typing import Optional, Protocol, Literal
from pydantic import BaseModel, Field
from datetime import datetime

class UserAlreadyExistsException(Exception):
    pass

class TelegramUser(BaseModel):
    id: str
    email: str
    username: str
    role: Literal["ADMIN", "USER"] = "USER"
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    def is_admin(self) -> bool:
        return self.role == "ADMIN"

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