from aiogram import types
from loguru import logger
from datab import *
from subprocess import Popen, PIPE
import io
import urllib.request as request

def commands(bot_dp):
    logger.info('Init main commands')
    @bot_dp.message_handler(commands=['start'])                                             # start
    async def send_welcome(message: types.Message):
        logger.info('Command /start from {}'.format(message.from_user.id))
        if check_user(message) == False: add_user(message)
        else: add_message(message)
        await message.reply("Hi!\nI'm <b>The vdsap Bot!</b>\nSee /help for avaliable commands")
        logger.debug('Message /start sent to {}'.format(message.from_user.id))



    @bot_dp.message_handler(commands=['help'])                                              # Help
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



    @bot_dp.message_handler(commands=['contact'])                                           # Contact to autor
    async def contact(message: types.Message):
        logger.info('Command /contact from {}'.format(message.from_user.id))
        if check_user(message) == False: add_user(message)
        else:
            add_message(message)
        await message.reply("""<a href='t.me/VDSap'>vdsap</a>""")
        logger.debug('Message /contact sent to {}'.format(message.from_user.id))
        update_user_info(message)



    @bot_dp.message_handler(commands=['info'])                                              # Get user stats
    async def info(message: types.Message):
        logger.info('Command /info from {}'.format(message.from_user.id))
        await message.reply(user_info(message))
        logger.debug('Message /info sent to {}'.format(message.from_user.id))
        update_user_info(message)



    @bot_dp.message_handler(commands=['addadmin'])                                           # Add admin
    async def addadmin(message: types.Message):
        logger.info('Command /addadmin from {}'.format(message.from_user.id))
        await message.reply(add_admin(message))
        update_user_info(message)



    @bot_dp.message_handler(commands=['removeadmin'])                                        # Remove admin
    async def removeadmin(message: types.Message):
        logger.info('Command /removeadmin from {}'.format(message.from_user.id))
        await message.reply(remove_admin(message))
        update_user_info(message)



    @bot_dp.message_handler(commands=['adminlist'])                                           # Admin list
    async def adminlist(message: types.Message):
        logger.info('Command /adminlist from {}'.format(message.from_user.id))
        if check_user(message) == False: add_user(message)
        else:
            add_message(message)
        await message.reply(admin_list())
        update_user_info(message)



    @bot_dp.message_handler(commands=['speedtest'])                                           # speedtest
    async def speedtest(message: types.Message):
        logger.info('Command /speedtest from {}'.format(message.from_user.id))
        if check_user(message) == False: add_user(message)
        else:
            add_message(message)
        if check_admin(message.from_user.id) == True or check_superadmin(message.from_user.id) == True:
            mes = await message.reply('Running speedtest...')
            logger.info('Running speedtest...')
            try:
                p = Popen(['speedtest-cli', '--simple'], stdout=PIPE, stderr=PIPE)
                out, err = p.communicate()
                await mes.edit_text(out.decode('utf-8'))
                logger.info('Speedtest done')
            except FileNotFoundError:
                await mes.edit_text('speedtest-cli not found')
                logger.error('speedtest-cli not found')
        else:
            await message.reply('You are not admin')
        update_user_info(message)




    @bot_dp.message_handler(commands=['get_schedule'])  # schedule
    async def getschedule(message: types.Message):
        logger.info('Command /get schedule from {}'.format(message.from_user.id))
        if check_user(message) == False: add_user(message)
        else:
            add_message(message)
        data = request.urlopen('https://cchgeu.ru/upload/iblock/d1c/93smt2hch2s73tzuwdc98njiur9im1tq/BSTR_2216.doc')
        file = io.BytesIO(data.read())
        file.seek(0)
        file.name = 'Расписание БСТР-2216.doc'
        await message.reply_document(file)
        update_user_info(message)




    # @bot_dp.message_handler()                                                                  # Any message
    # async def new_message(message:types.Message):
    #     logger.info('New Message from {}'.format(message.from_user.id))
    #     if check_user(message) == False: add_user(message)
    #     else:
    #         add_message(message)
    #     update_user_info(message)