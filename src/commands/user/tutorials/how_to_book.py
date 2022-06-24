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
            "*BOOK CLASSES ✨* \n\n"
            "Book any of the classes by selecting a date in the calendar. "
            "Then a list of classes will be displayed. \n\n"
            "Click on any of the classes to book it (or schedule). And click it again to cancel it. \n\n"
            "Scheduled classes will be booked for you, so you do't have to worry about alarms and booking classes in time. "
        ),
        parse_mode="Markdown"
    )
    await bot.send_video(
        chat, 
        "https://thumbs.gfycat.com/PotableSorrowfulAfghanhound-mobile.mp4",
    )