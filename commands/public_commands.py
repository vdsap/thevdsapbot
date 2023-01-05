from aiogram import types
from loguru import logger
import io
import urllib.request as request
from datab import *
def public(dp):
    logger.info('Init public commands')

    @dp.message_handler(commands=['get_schedule'])  # schedule
    async def getschedule(message: types.Message):
        logger.info('Command /get schedule from {}'.format(message.from_user.id))
        if check_user(message) == False:
            add_user(message)
        else:
            add_message(message)
        data = request.urlopen('https://cchgeu.ru/upload/iblock/d1c/93smt2hch2s73tzuwdc98njiur9im1tq/BSTR_2216.doc')
        file = io.BytesIO(data.read())
        file.seek(0)
        file.name = 'Расписание БСТР-2216.doc'
        await message.reply_document(file)
        update_user_info(message)


    @dp.message_handler(commands=['info'])                                              # Get user stats
    async def info(message: types.Message):
        logger.info('Command /info from {}'.format(message.from_user.id))
        await message.reply(user_info(message))
        logger.debug('Message /info sent to {}'.format(message.from_user.id))
        update_user_info(message)