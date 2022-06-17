from functools import wraps

def init(func):
    @wraps(func)
    async def wrapped(update, context):
        bot = context.bot
        if update.effective_message and update.effective_message.text is not None:
            await bot.delete_message(update.effective_message.chat_id, update.effective_message.message_id)
        return await func(update, context)
    return wrapped