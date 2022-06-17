from src.entities.booking import Booking
from src.infrastructure import user_repository

async def login(mail: str, pw: str) -> Booking:
    await user_repository.login(mail=mail, pw=pw)
