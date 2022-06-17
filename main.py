from fastapi import FastAPI

# from alphabot import bot
import asyncio

app = FastAPI()

import pytz  # type: ignore
from telegram.ext import (
    Updater,
    CommandHandler,
    Application,
)
from telegram import Update
from typing import Any
from src.commands.bot import add_public_commands

TOKEN = "5449340591:AAGQ05hp2NliXxz9zowlWVLUg-vZ-LsGeIM"

async def start(update: Update, context: Any) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text("Hi!")


# def start_telegram_bot() -> None:

#     # Get the dispatcher to register handlers
#     dsp: Dispatcher = updater.dispatcher  # type: ignore
#     job_updater: JobQueue = updater.job_queue  # type: ignore

#     # Load all commands
#     start_handler = CommandHandler("start", start)
#     add_public_commands(dsp)
#     dsp.add_handler(start_handler)


# async def start_telegram_app() -> None:
    # Create the Application and pass the bot's token

    # Add chat handlers

    # await telegram_app.initialize()
    # await telegram_app.start()



async def stop_telegram_app() -> None:
    await telegram_app.stop()


telegram_app = Application.builder().token(TOKEN).build()
add_public_commands(telegram_app)
telegram_app.add_handler(CommandHandler("start", start))
telegram_app.run_polling(close_loop=False)


@app.get("/")
def read_root():
    return {"Hello": "World"}


# @app.on_event("startup")
# async def startup_event():
#     await start_telegram_app()


@app.on_event("shutdown")
async def shutdown_event():
    await stop_telegram_app()
