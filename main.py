from fastapi import FastAPI

# from alphabot import bot
import asyncio

app = FastAPI()

import pytz  # type: ignore
from telegram.ext import (
    Updater,
    Defaults,
    CommandHandler,
    Dispatcher,
    JobQueue,
    Application,
)
from telegram import ParseMode, Update
from typing import Any
from src.controllers.bot_handlers import add_public_commands

TOKEN = "5449340591:AAGQ05hp2NliXxz9zowlWVLUg-vZ-LsGeIM"

# Create the Updater and pass it your bot's token.
updater = Updater(TOKEN, workers=10, use_context=True)


async def start(update: Update, context: Any) -> None:
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!"
    )


def start_telegram_bot() -> None:

    defaults = Defaults(
        parse_mode=ParseMode.HTML, tzinfo=pytz.timezone("Europe/Madrid")
    )

    # Get the dispatcher to register handlers
    dsp: Dispatcher = updater.dispatcher  # type: ignore
    job_updater: JobQueue = updater.job_queue  # type: ignore

    # Load all commands
    start_handler = CommandHandler("start", start)
    add_public_commands(dsp)
    dsp.add_handler(start_handler)

    updater.start_polling(poll_interval=1.0, timeout=10)


def start_telegram_app() -> None:
    # Create the Application and pass the bot's token
    app = Application.builder().token(TOKEN).build()

    # Add chat handlers


def stop_telegram_bot() -> None:
    updater.stop()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.on_event("startup")
async def startup_event():
    start_telegram_bot()


@app.on_event("shutdown")
async def shutdown_event():
    stop_telegram_bot()
