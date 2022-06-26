from telegram import Bot, Update

from src.utils.telegram_context import AlphaContext
from src.utils import decorators


@decorators.user
async def handler(update: Update, context: AlphaContext) -> None:
    
    if (not update.effective_message):
        return

    bot: Bot = context.bot
    chat = update.effective_message.chat_id

    await bot.send_chat_action(chat, "typing")

    await bot.send_message(
        chat,
        (
            "*FAQS* \n\n"
            "*What can I do with this bot?*\n"
            "Mostly make bookings like you do in aimharder. But also schedule bookings that are more than 4 days ahead.\n\n"

            "*How many classes can I schedule?*\n"
            "As many as you want. If you have 4 bookable classes a week, the bot will still try to book the class and fail if it exceeds the week bookings count.\n\n"

            "*Can I cancel a booking?*\n"
            "Yes, click on any of the classes that has (BOOKED) or (SCHEDULED) tags\n\n"

            "*How much time does the login lasts?*\n"
            "It lasts for 2 months. The bot will remind you to renew it.\n\n"

            "*What if a class gets deleted in aimharder and I had already scheduled it?*\n"
            "The bot will delete the scheduling for that class. \n\n"

        ),
        parse_mode="Markdown"
    )
