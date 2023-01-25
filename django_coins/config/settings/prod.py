from config.settings.base import *

DEBUG = False
ALLOWED_HOSTS = ['vkhmn.ru', 'coins.vkhmn.ru', '127.0.0.1']

USE_X_FORWARDED_HOST = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
CSRF_COOKIE_SECURE = True
CSRF_TRUSTED_ORIGINS = [f'https://coins.vkhmn.ru']
