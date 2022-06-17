from functools import wraps
from src.utils.functions import get_user_id_list
from src.infrastructure import telegram_user_repository


def init(func):
    @wraps(func)
    async def wrapped(update, context):

        if update.effective_user is None:
            return False

        user_id = str(update.effective_user.id)
        user = await telegram_user_repository.get_user_by_telegram_id(user_id)

        if not user:
            print("Unauthorized access denied for {}.".format(user_id))
            return
        
        # Add user email to context
        context.user_email = user.email

        return await func(update, context)
        
    return wrapped