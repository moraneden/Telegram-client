import telegram
from telegram.ext import Updater
import logging
from telegram.ext import CommandHandler, MessageHandler, Filters
import secrets


TOKEN = secrets.BOT_TOKEN

# bot = telegram.Bot(token=TOKEN)
# print(bot.get_me())


updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher


def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")


def echo(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text=update.message.text)


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)


def hello(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))


updater.dispatcher.add_handler(CommandHandler('hello', hello))

updater.start_polling()
updater.idle()


