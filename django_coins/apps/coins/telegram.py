from os import environ
from telebot import TeleBot
from telebot.apihelper import ApiTelegramException
from config.settings.dev import logger


TOKEN = environ.get('TOKEN')


def send_message(chat_id, message, image=None):
    logger.info('Start')
    logger.info(f'{message}')
    logger.info(f'{image}')
    bot = TeleBot(TOKEN)

    if image is None:
        msg = bot.send_message(chat_id, message, parse_mode='html')
    else:
        try:
            msg = bot.send_photo(chat_id, image, message, parse_mode='html')
        except ApiTelegramException as e:
            logger.error(e)
            return None

    logger.info('Finished')
    return msg.message_id
