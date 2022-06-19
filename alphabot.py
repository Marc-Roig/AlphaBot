from telegram.ext import Application, CallbackContext
from src.commands import add_user_commands, add_repeating_jobs
from src.infrastructure import start_beanie
import logging
import os

logger = logging.getLogger(__name__)


async def startup(context: CallbackContext) -> None:
    logger.info("Starting up database...")
    await start_beanie()
    logger.info("Database initialized")

def init_logger():

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    
    console_logger = logging.StreamHandler()
    console_logger.setLevel(logging.INFO)
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_logger.setFormatter(formatter)
    
    root_logger.addHandler(console_logger)

    logging.getLogger('telegram.bot').setLevel(logging.ERROR)
    logging.getLogger('telegram.ext.updater').setLevel(logging.ERROR)
    logging.getLogger('apscheduler.scheduler').setLevel(logging.ERROR)
    logging.getLogger('apscheduler.executors.default').setLevel(logging.ERROR)
    logging.getLogger('JobQueue').setLevel(logging.ERROR)


def main() -> None:

    init_logger()

    # Initialize the bot
    telegram_app = Application.builder().token(os.environ['TOKEN']).build()
    
    job_queue = telegram_app.job_queue
    job_queue.run_once(startup, 0)

    # Add handlers
    add_user_commands(telegram_app)
    add_repeating_jobs(telegram_app)

    # Run the bot
    telegram_app.run_polling()

if __name__ == "__main__":
    main()
