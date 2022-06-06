TOKEN = "5449340591:AAGQ05hp2NliXxz9zowlWVLUg-vZ-LsGeIM"

import telebot
from telebot.async_telebot import AsyncTeleBot
from telebot import types
from telebot.types import Message, CallbackQuery

bot = AsyncTeleBot(TOKEN, parse_mode=None) # You can set parse_mode by default. HTML or MARKDOWN

commands = {  # command description used in the "help" command
    'help'        : 'Gives you information about the available commands',
    'list' : 'List of all available classes to book',
}

# help page
@bot.message_handler(commands=['help'])
async def command_help(message: Message):
    cid = message.chat.id
    help_text = "The following commands are available: \n"
    for key in commands:  # generate help text out of the commands dictionary defined at the top
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    await bot.send_message(cid, help_text)  # send the generated help page


@bot.message_handler(commands=['list'])
async def list_classes(message: Message):
	markup = types.ReplyKeyboardMarkup(row_width=2)
	await bot.reply_to(message, "Here's a list of classes:")

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Yes", callback_data="cb_yes"),
                               InlineKeyboardButton("No", callback_data="cb_no"))
    return markup

@bot.callback_query_handler(func=lambda call: True)
async def callback_query(call: CallbackQuery):
    print(call.from_user.id)
    if call.data == "cb_yes":
        await bot.answer_callback_query(call.id, "Answer is Yes")
    elif call.data == "cb_no":
        await bot.answer_callback_query(call.id, "Answer is No")

@bot.message_handler(commands=['keyboard'])
async def message_handler(message):
    await bot.send_message(message.chat.id, "Yes/no?", reply_markup=gen_markup())



import asyncio
asyncio.run(bot.polling())
