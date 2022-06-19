from telegram.ext import Application, CallbackContext
from src.commands import add_user_commands, add_repeating_jobs

from src.infrastructure import start_beanie
import time
import logging
from pathlib import Path
from logging import handlers
import re
import sys
import os
logger = logging.getLogger(__name__)


TOKEN = "5449340591:AAGQ05hp2NliXxz9zowlWVLUg-vZ-LsGeIM"

async def startup(context: CallbackContext) -> None:
    print("Starting up database...")
    await start_beanie()
    print("Database initialized")
    service_initialized = True

def init_logger():
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    console_logger = logging.StreamHandler()
    console_logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_logger.setFormatter(formatter)
    root_logger.addHandler(console_logger)

    this_file_name = os.path.basename(os.path.splitext(os.path.basename(__file__))[0])

    Path('./logs/').mkdir(parents=True, exist_ok=True)
    logfile = './logs/' + this_file_name

    file_logger = handlers.TimedRotatingFileHandler(logfile, encoding='utf-8', when='midnight')
    file_logger.suffix = "%Y-%m-%d.log"
    file_logger.extMatch = re.compile(r'^\d{4}-\d{2}-\d{2}\.log$')
    file_logger.setLevel(logging.DEBUG)
    file_logger.setFormatter(formatter)
    root_logger.addHandler(file_logger)

    logging.getLogger('telegram.bot').setLevel(logging.INFO)
    logging.getLogger('telegram.ext.updater').setLevel(logging.INFO)
    logging.getLogger('JobQueue').setLevel(logging.INFO)

    return logfile

def main() -> None:

    init_logger()

    # Initialize the bot
    telegram_app = Application.builder().token(TOKEN).build()
    
    job_queue = telegram_app.job_queue
    job_queue.run_once(startup, 0)

    # Add handlers
    add_user_commands(telegram_app)
    add_repeating_jobs(telegram_app)

    # Run the bot
    telegram_app.run_polling()

print('Initializing...')

if __name__ == "__main__":
    main()
