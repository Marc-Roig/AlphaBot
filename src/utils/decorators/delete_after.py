from functools import wraps

def init(func):
    """
    Deletes the message after the function has been executed
    """
    @wraps(func)
    async def wrapped(update, context):
        bot = context.bot
        result = await func(update, context)
        if update.effective_message and update.effective_message.text is not None:
            await bot.delete_message(update.effective_message.chat_id, update.effective_message.message_id)
        return result
    return wrapped