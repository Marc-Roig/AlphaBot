from src.infrastructure import telegram_user_repository

async def get_user_id_list() -> list[str]:
    return await telegram_user_repository.get_all_user_ids()