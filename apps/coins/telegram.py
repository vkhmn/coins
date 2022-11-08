from os import environ
from telebot import TeleBot


TOKEN = environ.get('TOKEN')


def send_message(chat_id, message, image=None):
    bot = TeleBot(TOKEN)

    if image is None:
        msg = bot.send_message(chat_id, message)
    else:
        msg = bot.send_photo(chat_id, image, message, parse_mode='Markdown')
    print(msg)

    return msg.message_id
