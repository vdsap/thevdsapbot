from aiogram import types
from loguru import logger
from subprocess import Popen, PIPE

def commands(dp):
    logger.info('Init main commands')
    @dp.message_handler(commands=['start'])                                             # start
    async def send_welcome(message: types.Message):
        logger.info('Command /start from {}'.format(message.from_user.id))
        if check_user(message) == False: add_user(message)
        else: add_message(message)
        await message.reply("Hi!\nI'm <b>The vdsap Bot!</b>\nSee /help for avaliable commands")
        logger.debug('Message /start sent to {}'.format(message.from_user.id))



    @dp.message_handler(commands=['help'])                                              # Help
    async def send_help(message: types.Message):
        logger.info('Command /help from {}'.format(message.from_user.id))
        await message.reply("""Avaliable commands:
/start: Start bot
/help: list of avaliable commands
/speedtest: Run speedtest
/info: Get user stats
/addadmin: Add user to admins
/removeadmin: Remove user from admins
/adminlist: Get list of admins
/contact: Write to autor""")
        if check_user(message) == False: add_user(message)
        else:
            add_message(message)
        logger.debug('Message /help sent to {}'.format(message.from_user.id))
        update_user_info(message)



    @dp.message_handler(commands=['contact'])                                           # Contact to autor
    async def contact(message: types.Message):
        logger.info('Command /contact from {}'.format(message.from_user.id))
        if check_user(message) == False: add_user(message)
        else:
            add_message(message)
        await message.reply("""<a href='t.me/VDSap'>vdsap</a>""")
        logger.debug('Message /contact sent to {}'.format(message.from_user.id))
        update_user_info(message)

