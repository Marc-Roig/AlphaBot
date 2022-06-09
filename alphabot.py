TOKEN = "5449340591:AAGQ05hp2NliXxz9zowlWVLUg-vZ-LsGeIM"

from datetime import datetime
from typing import Any
import telebot
from telebot.async_telebot import AsyncTeleBot
from telebot import types
from telebot.types import Message, CallbackQuery
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.use_cases.list_daily_classes import list_daily_classes

bot = AsyncTeleBot(
    TOKEN, parse_mode=None
)  # You can set parse_mode by default. HTML or MARKDOWN

commands = {  # command description used in the "help" command
    "help": "Gives you information about the available commands",
    "hello": "List of all available commands",
    "list": "List of all available classes to book",
}

# help page
@bot.message_handler(commands=["help"])
async def command_help(message: Message) -> None:
    cid = message.chat.id
    help_text = "The following commands are available: \n"
    # generate help text out of the commands dictionary defined at the top
    for key in commands:
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    await bot.send_message(cid, help_text)  # send the generated help page


def gen_markup() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("🏋🏻‍♀️ Today's classes", callback_data="list_class"),
        InlineKeyboardButton("💪 Book class", callback_data="book"),
    )
    return markup


@bot.message_handler(func=lambda message: message.text == "hello")
async def message_handler(message: Message) -> None:
    await bot.send_message(message.chat.id, "Pick one!", reply_markup=gen_markup())


@bot.message_handler(commands=["list"])
async def list_classes(message: Message) -> None:
    markup = types.ReplyKeyboardMarkup(row_width=2)
    await bot.reply_to(message, "Here's a list of classes:")


@bot.callback_query_handler(func=lambda call: True)
async def callback_query(call: CallbackQuery) -> None:
    print(call.from_user.id)
    if call.data == "list_class":

        bookings = await list_daily_classes(
            datetime.today(),
            "marc12info@gmail.com",
            [
                "WOD",
                "FITCOND",
                "WOD WEEK-END",
                "FITCOND WEEK-END",
                "WEIGHTLIFTING",
                "GYMNASTICS",
            ],
        )

        text = "Here's a list of classes: \n\n"
        for booking in bookings:
            text += f" {booking.start_timestamp.strftime('%H:%M')}h - {booking.class_name} \n"
        await bot.send_message(call.message.chat.id, text, parse_mode="HTML")

    elif call.data == "book":
        await bot.answer_callback_query(call.id, "Answer is No")


@bot.message_handler(commands=["keyboard"])
async def keyboard_handler(message: Message) -> None:
    keyboard = [
        [
            InlineKeyboardButton("Option 1", callback_data="1"),
            InlineKeyboardButton("Option 2", callback_data="2"),
        ],
        [InlineKeyboardButton("Option 3", callback_data="3")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await bot.send_message(message.chat.id, "Please choose:", reply_markup=reply_markup)


import asyncio

asyncio.run(bot.polling(non_stop=True))
