from telegram import Update
from telegram.ext import ConversationHandler
from src.utils import decorators
from src.utils.telegram_context import AlphaContext
from src.infrastructure import telegram_user_repository
import asyncio

START = 0

@decorators.admin
async def handler_start(update: Update, context: AlphaContext) -> int:
    
    if (not update.effective_message):
        return ConversationHandler.END

    bot = context.bot
    chat = update.effective_message.chat_id

    await bot.send_chat_action(chat, "typing")
    await bot.send_message(chat, "Type message")

    return START


@decorators.admin
async def handler_message(update: Update, context: AlphaContext) -> int:

    if (not update.effective_message):
        return ConversationHandler.END

    bot = context.bot
    chat = update.effective_message.chat_id
    message = update.effective_message.text

    await bot.send_chat_action(chat, "typing")

    # Get all users registered
    users_id = await telegram_user_repository.get_all_user_ids()
    user_message_promises = []

    try:
        # Send message to all users
        for user_id in users_id:
            user_message_promises.append(
                bot.send_message(user_id, message, parse_mode="Markdown")
            )
            
        await asyncio.gather(*user_message_promises)

    except Exception as e:
        await bot.send_message(chat, "❌ Something went wrong. Broadcast failed.")

    await bot.send_message(chat, "✅ Message sent to all users")

    return ConversationHandler.END

@decorators.admin
async def handler_cancel(update: Update, context: AlphaContext) -> int:

    if (not update.effective_message):
        return ConversationHandler.END

    # Cancels and ends the conversation.
    await update.effective_message.reply_text(
        "❌ Something went wrong. Broadcast failed.",
    )

    return ConversationHandler.END