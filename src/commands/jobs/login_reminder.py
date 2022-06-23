"""
Any request to AimHarder requires a token that is generated when the user is logged in.

The process to generate and store the token in this app is:
- User uses the /login command
- The bot sends a message asking for a password
- User enters the password
- The password and the user email are used to log in to Aimharder
- The returned token is stored in the database (if there is one)

Once every 2 months, the bot will send a reminder to the user to log in. 
As this token expires in that time.
"""
from telegram.ext import CallbackContext
from src.infrastructure import user_repository, telegram_user_repository
import datetime

async def handler(context: CallbackContext) -> None:

    # Find users where the last update was more than 2 months ago    
    users = await user_repository.get_all()

    for user in users:
        if user.updated_at < datetime.datetime.now(user.updated_at.tzinfo) - datetime.timedelta(days=60):
            # Get the telegram user before notifying the user
            telegram_user = await telegram_user_repository.get_user_by_email(user.email)
            if not telegram_user:
                continue

            await context.bot.send_message(
                telegram_user.id, 
                f"🤖❌ Your AimHarder login is about to expire. Please log in again (/login)."
            )
