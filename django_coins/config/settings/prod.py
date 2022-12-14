from config.settings.base import *

DEBUG = False
ALLOWED_HOSTS = ['vkhmn.ru', 'coins.vkhmn.ru', '127.0.0.1']

SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'https')