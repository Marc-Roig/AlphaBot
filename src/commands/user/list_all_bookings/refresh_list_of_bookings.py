from telegram import Update, Bot
from telegram import InlineKeyboardMarkup

from src.utils import decorators
from src.utils.telegram_context import AlphaContext
from src.commands.user.list_all_bookings.list_all_bookings import _get_booked_classes, _get_message_menu

@decorators.user
async def handler(update: Update, context: AlphaContext) -> None:
    
    if (not update.effective_message) or (not context.user_email):
        return
 
    bot: Bot = context.bot
    chat = update.effective_message.chat_id
    query = update.callback_query
    
    await query.answer()
    await bot.send_chat_action(chat, "typing")

    # Get list of bookings for the user
    text = await _get_booked_classes(context.user_email)

    # Buttons to close and refresh list
    menu = _get_message_menu()
    
    try:
        await bot.edit_message_text(
            text, 
            chat, 
            update.effective_message.message_id, reply_markup=InlineKeyboardMarkup(menu),
            parse_mode="Markdown"
        )
    except:
        pass