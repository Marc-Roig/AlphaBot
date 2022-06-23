from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ConversationHandler
import re
from src.output_ports.telegram_user_port import TelegramUser
from src.utils.menu import build_menu

from src.utils.telegram_context import AlphaContext
from src.infrastructure import telegram_user_repository
from src.utils import decorators

START = 0


async def start(update: Update, context: AlphaContext) -> int:

    if (not update.effective_message) :
        return ConversationHandler.END

    bot: Bot = context.bot
    chat = update.effective_message.chat_id
    
    await bot.send_chat_action(chat, "typing")

    await update.effective_message.reply_text((\
        "Hello! This is AlphaBot, I am here to help you book classes at Alpha Link Crossfit. \n\n"
        "Before starting, an admin has to grant you access. Please type your *aimharder* email:"
    ), parse_mode="Markdown")

    return START


async def _ask_admin_for_invite(bot: Bot, admin_id: str, user_mail: str, user_id: int) -> None:

    buttons  = [
        InlineKeyboardButton("✅ Accept", callback_data=f"accept_invite;{user_mail};{user_id}"),
        InlineKeyboardButton("❌ Decline", callback_data=f"decline_invite;{user_mail};{user_id}"),
    ]
    menu = build_menu(buttons, n_cols=2)
    await bot.send_message(admin_id, f"{user_mail} is asking for an invite.", reply_markup=InlineKeyboardMarkup(menu))


async def send_email(update: Update, context: AlphaContext) -> int:
    
    if (not update.effective_message):
        return ConversationHandler.END
    
    bot: Bot = context.bot
    chat = update.effective_message.chat_id
    email = update.effective_message.text

    # Validate with regex the message is a valid email
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        await bot.send_message(chat, "❌ This seems not to be a valid email format. Please type it again.")
        return START

    # Send message to an admin
    admins = await telegram_user_repository.get_all_admin_ids()
    if admins:
        await _ask_admin_for_invite(bot, admins[0], email, chat)
        
    # End conversation
    await bot.send_message(chat, "✅ Please wait for an admin to grant you access.")
    return ConversationHandler.END


async def cancel(update: Update, context: AlphaContext) -> int:

    if (not update.effective_message):
        return ConversationHandler.END

    # Cancels and ends the conversation
    await update.effective_message.reply_text(
        "❌ Something went wrong. Try again.",
    )

    return ConversationHandler.END


@decorators.admin
@decorators.delete
async def accept_invitation(update: Update, context: AlphaContext) -> None:
    
    if (not update.effective_message):
        return

    bot: Bot = context.bot
    chat: int = update.effective_message.chat_id
    query = update.callback_query

    await query.answer()
    await bot.send_chat_action(chat, "typing")

    # Get the email from the callback data
    _, mail, user_id = query.data.split(";")
    # Add user to the database
    try:
        await telegram_user_repository.add_user(
            TelegramUser(
                id=user_id,
                email=mail,
                username=mail, # TODO: get username
            )
        )
        # Notify admin
        await bot.send_message(chat, f"✅ {mail} has been added to the database.")
        # Notify user
        await bot.send_message(
            user_id, 
            (f"🎉 You have been accepted! You can now book classes."
            "Use /help to see the list of commands.")
        )

    except:
        # Notify admin
        await bot.send_message(chat, "❌ Something went wrong. Discarding the invitation.")
        # Notify user
        await bot.send_message(user_id, "❌ Something went wrong. Your invitation was discarded form some reason. Try again")


@decorators.admin
@decorators.delete
async def decline_invitation(update: Update, context: AlphaContext) -> None:
    
    if (not update.effective_message):
        return

    bot: Bot = context.bot
    chat: int = update.effective_message.chat_id
    query = update.callback_query

    await query.answer()
    await bot.send_chat_action(chat, "typing")

    # Get the email from the callback data
    _, mail, user_id = query.data.split(";")

    # Notify admin
    await bot.send_message(chat, f"❌ Discarded invitation for {mail}.")
    # Notify user
    await bot.send_message(user_id, f"😔 Your request to use AlphaBot has been rejected.")