#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import pymongo
import logging

from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["beloter"]
mycol = mydb["users"]

keyRound = [
        [
            InlineKeyboardButton("\U0001F534 -10", callback_data='r-10'),
            InlineKeyboardButton("\U0001F534 -5", callback_data='r-5'),
            InlineKeyboardButton("\U0001F534 -1", callback_data='r-1'),
            InlineKeyboardButton("\U0001F534 +1", callback_data='r1'),
            InlineKeyboardButton("\U0001F534 +5", callback_data='r5'),
            InlineKeyboardButton("\U0001F534 +10", callback_data='r10'),
        ],
        [
            InlineKeyboardButton("\U0001F7E2 -10", callback_data='g-10'),
            InlineKeyboardButton("\U0001F7E2 -5", callback_data='g-5'),
            InlineKeyboardButton("\U0001F7E2 -1", callback_data='g-1'),
            InlineKeyboardButton("\U0001F7E2 +1", callback_data='g1'),
            InlineKeyboardButton("\U0001F7E2 +5", callback_data='g5'),
            InlineKeyboardButton("\U0001F7E2 +10", callback_data='g10'),
        ],
        [
            InlineKeyboardButton("\U0001F534 BT", callback_data='rb'),
            InlineKeyboardButton("\U0001F7E2 BT", callback_data='gb'),
            InlineKeyboardButton("\U000025B6", callback_data='go'),
        ],
    ]
markRound = InlineKeyboardMarkup(keyRound)
# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.

def sumaBile(score, mod):
    splitx = score.split(' ')
    r = int(splitx[0])
    g = int(splitx[1])
    if mod[:1]=='r':
        r += int(mod[1:])
    if mod[:1]=='g':
        g += int(mod[1:])
    return str(r)+" "+str(g)

def start(update, context):
    keyStart = [
        [
        InlineKeyboardButton("\U0001F3C1 New 3 game", callback_data='r'),
        InlineKeyboardButton("\U0001F3C1 New 4 game", callback_data='r'),
        ],
    ]
    markStart = InlineKeyboardMarkup(keyStart)
    """Send a message when the command /start is issued."""
    update.message.reply_text('y', reply_markup=markStart)

def button(update, context) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()
    
    query.edit_message_text(sumaBile(query.message.text,query.data) , reply_markup=markRound)

def buttons(update, context) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()
    
    query.edit_message_text("LOL", reply_markup=markRound)

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update, context):
    user = update.message.from_user
    myque = {"username":user['username']}
    splitx = update.message.text.split(' ')
    if update.message.text == "x":
        myset = {"$set":{"score":[]}}
        x = mycol.update_one(myque, myset, upsert=True)
    if len(splitx)==2:
        split0 = splitx[0]
        split1 = splitx[1]
        if (split0 + split1).isnumeric():
            mypush = {"$push":{"score":[split0,split1]}}
            x = mycol.update_one(myque, mypush, upsert=True)
            a = ""
            sum1 = 0
            sum2 = 0
            for x in mycol.find_one(myque)["score"]:
                a += (x[0]+" "+x[1]+"\n")
                sum1 += int(x[0])
                sum2 += int(x[1])
            update.message.reply_text(a)
            a = str(sum1)+" "+str(sum2)
            update.message.reply_text(a, reply_markup=markRound)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("2002310200:AAHGQcQA6N7j6Y8YV7KL9b-52sMQ5U-vWCo", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    dp.add_handler(CallbackQueryHandler(button, pattern='[rg]'))
    dp.add_handler(CallbackQueryHandler(buttons, pattern='[s]'))
    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
