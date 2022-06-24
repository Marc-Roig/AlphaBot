from telegram import Bot, Update
from src.output_ports.telegram_user_port import TelegramUser
from src.utils.telegram_context import AlphaContext
from src.infrastructure import telegram_user_repository
from src.utils import decorators


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