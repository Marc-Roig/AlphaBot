from telegram.ext import Application, CallbackContext
from src.commands import add_user_commands, add_repeating_jobs

from src.infrastructure import start_beanie
import time

TOKEN = "5449340591:AAGQ05hp2NliXxz9zowlWVLUg-vZ-LsGeIM"

async def startup(context: CallbackContext) -> None:
    await start_beanie()
    print("Database initialized")
    service_initialized = True


def main() -> None:

    # Initialize the bot
    telegram_app = Application.builder().token(TOKEN).build()
    
    job_queue = telegram_app.job_queue
    job_queue.run_once(startup, 0)

    # Add handlers
    add_user_commands(telegram_app)
    add_repeating_jobs(telegram_app)

    # Run the bot
    telegram_app.run_polling()


if __name__ == "__main__":
    main()
