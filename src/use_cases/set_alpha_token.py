from src.entities.booking import Booking
from src.infrastructure import user_repository

async def set_user_alpha_token(mail: str, token: str) -> Booking:
    await user_repository.set_auth_cookie(mail=mail, amhrdauth=token)
