from pydantic.main import BaseModel
from typing import Literal, Optional

class UserAlreadyExistsException(Exception):
    pass

class TelegramUser(BaseModel):
    id: str
    email: str
    username: str
    role: Literal["ADMIN", "USER"] = "USER"

class TelegramUserRepository:
    
    user_tg: list[TelegramUser] = [
        TelegramUser(id="1089244954", email="marc12info@gmail.com", username="marcRoig", role="ADMIN"),
        TelegramUser(id="962171740", email="glezgutierrez95@gmail.com", username="glezGutierrez", role="ADMIN"),
    ]

    async def add_user(self, user: TelegramUser) -> None:
        # if user id is repeated
        for u in self.user_tg:
            if u.id == user.id:
                raise UserAlreadyExistsException("User id is repeated")

        self.user_tg.append(user)

    async def remove_user(self, telegram_id: str) -> None:
        for user in self.user_tg:
            if user.id == telegram_id:
                self.user_tg.remove(user)
                return

    async def get_user_by_telegram_id(self, telegram_id: str) -> Optional[TelegramUser]:
        for user in self.user_tg:
            if user.id == telegram_id:
                return user
        return None

    async def get_all_user_ids(self) -> list[str]:
        return [user.id for user in self.user_tg]

    async def get_all_admin_ids(self) -> list[str]:
        return [user.id for user in self.user_tg if user.role == "ADMIN"]
