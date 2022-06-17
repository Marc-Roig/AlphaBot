from typing import Any, Optional, Tuple
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove, Update, Bot
import datetime
import calendar

# Query Handler pattern
QH_CALENDAR_PATTERN = "DAY|PREV-MONTH|NEXT-MONTH|IGNORE"

def create_callback_data(action,year,month,day):
    """ Create the callback data associated to each button"""
    return ";".join([action,str(year),str(month),str(day)])

def separate_callback_data(data):
    """ Separate the callback data"""
    return data.split(";")


def create_calendar(year=None,month=None):
    """
    Create an inline keyboard with the provided year and month
    :param int year: Year to use in the calendar, if None the current year is used.
    :param int month: Month to use in the calendar, if None the current month is used.
    :return: Returns the InlineKeyboardMarkup object with the calendar.
    """

    now = datetime.datetime.now()
    if year == None: year = now.year
    if month == None: month = now.month
    
    data_ignore = create_callback_data("IGNORE", year, month, 0)

    # Keyboard create
    keyboard = []

    # First row - Month and Year
    row=[]
    row.append(
        InlineKeyboardButton(
            calendar.month_name[month] + " " + str(year),
            callback_data=data_ignore
        )
    )
    keyboard.append(row)
    
    #Second row - Week Days
    row=[]
    for day in ["Mo","Tu","We","Th","Fr","Sa","Su"]:
        row.append(InlineKeyboardButton(day,callback_data=data_ignore))
    keyboard.append(row)

    # Day numbers
    my_calendar = calendar.monthcalendar(year, month)
    for week in my_calendar:
        row=[]
        for day in week: # type: ignore
            if(day==0): #type: ignore 
                row.append(InlineKeyboardButton(" ", callback_data=data_ignore))
            else:
                text = str(day)
                # Check if day is today
                if year == now.year and month == now.month and int(day) == now.day:
                    text = "<" + text + ">"
                row.append(
                    InlineKeyboardButton(
                        text,
                        callback_data=create_callback_data("DAY",year,month,day)
                    )
                )
        keyboard.append(row)

    #Last row - Buttons
    row=[]
    row.append(InlineKeyboardButton("<",callback_data=create_callback_data("PREV-MONTH",year,month,day)))
    row.append(InlineKeyboardButton(" ",callback_data=data_ignore))
    row.append(InlineKeyboardButton(">",callback_data=create_callback_data("NEXT-MONTH",year,month,day)))
    keyboard.append(row)

    return InlineKeyboardMarkup(keyboard)


async def process_calendar_selection(bot: Bot, update: Update) -> Optional[datetime.datetime]:
    """
    Process the callback_query. This method generates a new calendar if forward or
    backward is pressed. This method should be called inside a CallbackQueryHandler.
    :param telegram.Bot bot: The bot, as provided by the CallbackQueryHandler
    :param telegram.Update update: The update, as provided by the CallbackQueryHandler
    :return: Returns selected date
    """

    query = update.callback_query

    (action, year, month, day) = separate_callback_data(query.data)
    curr = datetime.datetime(int(year), int(month), 1)
    
    if action == "IGNORE":
        await bot.answer_callback_query(callback_query_id= query.id)

    elif action == "DAY":
        # await bot.edit_message_text(text=query.message.text,
        #     chat_id=query.message.chat_id,
        #     message_id=query.message.message_id
        #     )
        return datetime.datetime(int(year),int(month),int(day))
    
    elif action == "PREV-MONTH":
        pre = curr - datetime.timedelta(days=1)
        await bot.edit_message_text(text=query.message.text,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            reply_markup=create_calendar(int(pre.year),int(pre.month)))
    
    elif action == "NEXT-MONTH":
        ne = curr + datetime.timedelta(days=31)
        await bot.edit_message_text(text=query.message.text,
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            reply_markup=create_calendar(int(ne.year),int(ne.month)))
    
    else:
        await bot.answer_callback_query(callback_query_id= query.id,text="Something went wrong!")

    return None