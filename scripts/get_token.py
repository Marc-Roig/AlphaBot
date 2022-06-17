"""
Make a booking when receiving a message like 10:00h | 22-06-13 | WOD
"""
from telegram import Update
from telegram.ext import ConversationHandler

from src.utils import decorators
from src.utils.telegram_context import AlphaContext
from src.use_cases.set_alpha_token import set_user_alpha_token as set_alpha_token_uc


START = 0

@decorators.user
async def start(update: Update, context: AlphaContext) -> int:

    if (not update.effective_message) :
        return ConversationHandler.END

    await update.effective_message.reply_text(
        "Type your new token:"
    )

    return START


@decorators.user
async def get_password(update: Update, context: AlphaContext) -> int:
    
    if (not update.effective_message) or (not context.user_email):
        return ConversationHandler.END

    bot = context.bot
    chat = update.effective_message.chat_id
    message = update.effective_message.text
    
    await bot.send_chat_action(chat, "typing")

    try:
        await set_alpha_token_uc(mail=context.user_email, token=message)
        await bot.send_message(chat, "✅ Token set")
    except:
        await bot.send_message(chat, "❌ Something went wrong. Token was not set.")
    
    return ConversationHandler.END


@decorators.user
async def cancel(update: Update, context: AlphaContext) -> int:

    if (not update.effective_message):
        return ConversationHandler.END

    """Cancels and ends the conversation."""
    await update.effective_message.reply_text(
        "❌ Token not set.",
    )

    return ConversationHandler.END
