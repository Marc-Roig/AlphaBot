from telegram import ReplyKeyboardRemove, Update, Bot

from src.commands.user.make_bookings.list_classes import delete_last_select_message
from src.utils.telegram_context import AlphaContext
from src.utils import decorators

@decorators.user
@decorators.delete
async def handler(update: Update, context: AlphaContext) -> None:

    if (not update.effective_message) or (not context.user_email):
        return
    
    bot: Bot = context.bot
    chat = update.effective_message.chat_id

    message = await bot.send_message(chat, "Booking discarded", reply_markup=ReplyKeyboardRemove())
    await delete_last_select_message(chat, context)
    await message.delete()

