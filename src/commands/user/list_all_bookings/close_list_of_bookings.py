from telegram import Update, Bot

from src.utils import decorators
from src.utils.telegram_context import AlphaContext


@decorators.user
async def handler(update: Update, context: AlphaContext) -> None:
    
    if (not update.effective_message) or (not context.user_email):
        return
 
    bot: Bot = context.bot
    chat = update.effective_message.chat_id
    query = update.callback_query
    
    await query.answer()
    await bot.delete_message(chat, update.effective_message.message_id)
    print("Closing list of bookings")