from telegram import Update
from telegram.ext import ConversationHandler
from src.output_ports.user_port import CredentialsError

from src.utils import decorators
from src.utils.telegram_context import AlphaContext
from src.use_cases.login import login as login_uc

START = 0

@decorators.user
async def start_handler(update: Update, context: AlphaContext) -> int:

    if (not update.effective_message) :
        return ConversationHandler.END

    await update.effective_message.reply_text(
        "Type your aimharder password:"
    )

    return START


@decorators.delete
@decorators.user
async def login_handler(update: Update, context: AlphaContext) -> int:
    
    if (not update.effective_message) or (not context.user_email):
        return ConversationHandler.END

    bot = context.bot
    chat = update.effective_message.chat_id
    message = update.effective_message.text
    
    await bot.send_chat_action(chat, "typing")

    try:
        await login_uc(mail=context.user_email, pw=message)
        await bot.send_message(chat, "✅ Logged in")
    except CredentialsError:
        await bot.send_message(chat, "❌ Wrong password. Login failed.")
    except:
        await bot.send_message(chat, "❌ Something went wrong. Login failed.")
    
    return ConversationHandler.END


@decorators.user
async def cancel_handler(update: Update, context: AlphaContext) -> int:

    if (not update.effective_message):
        return ConversationHandler.END

    """Cancels and ends the conversation."""
    await update.effective_message.reply_text(
        "❌ Something went wrong. Login failed.",
    )

    return ConversationHandler.END
