from aiogram import types
from loguru import logger
import io
import urllib.request as request
from datab import *
import requests


def public(dp):
    logger.info('Init public commands')

    # @dp.message_handler(commands=['get_schedule'])  # schedule
    # async def getschedule(message: types.Message):
    #     logger.info('Command /get schedule from {}'.format(message.from_user.id))
    #     if not check_user(message):
    #         add_user(message)
    #     else:
    #         add_message(message)
    #     data = request.urlopen('https://cchgeu.ru/upload/iblock/d1c/93smt2hch2s73tzuwdc98njiur9im1tq/BSTR_2216.doc')
    #     file = io.BytesIO(data.read())
    #     file.seek(0)
    #     file.name = 'Расписание БСТР-2216.doc'
    #     await message.reply_document(file)
    #     update_user_info(message)

    @dp.message_handler(commands=['info'])  # Get user stats
    async def info(message: types.Message):
        logger.info('Command /info from {}'.format(message.from_user.id))
        await message.reply(user_info(message))
        logger.debug('Message /info sent to {}'.format(message.from_user.id))
        update_user_info(message)

    @dp.message_handler(commands=['$', 'dollar'])  # $->₽
    async def dollar(message: types.Message):
        logger.info('Command /$ from {}'.format(message.from_user.id))
        if not check_user(message):
            add_user(message)
        else:
            add_message(message)
        try:
            arg = int(message.text.split(' ', 1)[1])
        except IndexError:
            arg = 1
        full = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
        value = full["Valute"]["USD"]["Value"]
        if arg == 1:
            await message.reply('<b>1$ --> {}₽</b>'.format(value))
        else:
            await message.reply(f'{round(value, 1)}₽\n<b>${str(arg)} --> {str(round(arg * float(value), 1))}₽</b>')
        update_user_info(message)

    @dp.message_handler(commands=['€', 'euro'])  # €->₽
    async def euro(message: types.Message):
        logger.info('Command /$ from {}'.format(message.from_user.id))
        if not check_user(message):
            add_user(message)
        else:
            add_message(message)
        try:
            arg = int(message.text.split(' ', 1)[1])
        except IndexError:
            arg = 1
        full = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
        value = full["Valute"]["EUR"]["Value"]
        if arg == 1:
            await message.reply('<b>1€ --> {}₽</b>'.format(value))
        else:
            await message.reply(f'{round(value, 1)}₽\n<b>€{str(arg)} --> {str(round(arg * float(value), 1))}₽</b>')
        update_user_info(message)

    # @dp.message_handler(commands=['uah', 'grn', '₴'])  # ₴->₽
    # async def uah(message: types.Message):
    #     logger.info('Command /$ from {}'.format(message.from_user.id))
    #     if not check_user(message):
    #         add_user(message)
    #     else:
    #         add_message(message)
    #     try:
    #         arg = int(message.text.split(' ', 1)[1])
    #     except IndexError:
    #         arg = 1
    #     full = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
    #     value = full["Valute"]["UAH"]["Value"] / 10
    #     if arg == 1:
    #         await message.reply('<b>1₴ --> {}₽</b>'.format(value))
    #     else:
    #         await message.reply(f'{round(value, 1)}₽\n<b>₴{str(arg)} --> {str(round(arg * float(value), 1))}₽</b>')
    #     update_user_info(message)
