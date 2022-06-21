from beanie import Document, Indexed
from pymongo import errors
from typing import Literal, Optional
from datetime import datetime
from pydantic import Field

from src.output_ports.telegram_user_port import TelegramUser, TelegramUserPort, UserAlreadyExistsException

class TelegramUsers(Document):
    userId: Indexed(str, unique=True) # type: ignore
    email: str
    username: str
    role: Literal["ADMIN", "USER"] = "USER"
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

def db_to_domain(telegram_user_db: TelegramUsers) -> TelegramUser:
    return TelegramUser(
        id=telegram_user_db.userId,
        email=telegram_user_db.email,
        username=telegram_user_db.username,
        role=telegram_user_db.role,
        created_at=telegram_user_db.created_at,
        updated_at=telegram_user_db.updated_at,
    )

def domain_to_db(telegram_user: TelegramUser) -> TelegramUsers:
    return TelegramUsers(
        userId=telegram_user.id,
        email=telegram_user.email,
        username=telegram_user.username,
        role=telegram_user.role,
        created_at=telegram_user.created_at,
    )

class TelegramUserMongoRepository(TelegramUserPort):
    
    async def add_user(self, user: TelegramUser) -> None:
        user_db = domain_to_db(user)
        try:
            await user_db.create()
        except errors.DuplicateKeyError:
            raise UserAlreadyExistsException("User id is repeated")

    async def remove_user(self, telegram_id: str) -> None:
        user = await TelegramUsers.find_one(TelegramUsers.userId == telegram_id)
        if user:
            await user.delete()       

    async def get_user_by_telegram_id(self, telegram_id: str) -> Optional[TelegramUser]:
        user = await TelegramUsers.find_one(TelegramUsers.userId == telegram_id)
        if user:
            return db_to_domain(user)
        return None

    async def get_user_by_email(self, email: str) -> Optional[TelegramUser]:
        user = await TelegramUsers.find_one(TelegramUsers.email == email)
        if user:
            return db_to_domain(user)
        return None

    async def get_all_user_ids(self) -> list[str]:
        users = await TelegramUsers.find().to_list()
        return [user.userId for user in users]

    async def get_all_admin_ids(self) -> list[str]:
        users = await TelegramUsers.find(TelegramUsers.role == "ADMIN").to_list()
        return [user.userId for user in users]