from aiogram import types
from loguru import logger
from datab import *

def message_commands(dp):
    logger.info('Init message commands')

    @dp.message_handler(commands=['addadmin'])  # Add admin
    async def addadmin(message: types.Message):
        logger.info('Command /addadmin from {}'.format(message.from_user.id))
        await message.reply(add_admin(message))
        update_user_info(message)

    @dp.message_handler(commands=['removeadmin'])  # Remove admin
    async def removeadmin(message: types.Message):
        logger.info('Command /removeadmin from {}'.format(message.from_user.id))
        await message.reply(remove_admin(message))
        update_user_info(message)

    @dp.message_handler(commands=['adminlist'])  # Admin list
    async def adminlist(message: types.Message):
        logger.info('Command /adminlist from {}'.format(message.from_user.id))
        if check_user(message) == False:
            add_user(message)
        else:
            add_message(message)
        await message.reply(admin_list())
        update_user_info(message)

    @dp.message_handler(commands=['speedtest'])  # speedtest
    async def speedtest(message: types.Message):
        logger.info('Command /speedtest from {}'.format(message.from_user.id))
        if check_user(message) == False:
            add_user(message)
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

    @bot_dp.message_handler(commands=['t', 'terminal', 'т'])  # Terminal
    async def terminal(message: types.Message):
        logger.info('Command /terminal from {}'.format(message.from_user.id))
        if check_user(message) == False:
            add_user(message)
        else:
            add_message(message)
        if check_superadmin(message.from_user.id) == True or check_admin(message) == True:
            command = message.text.split(' ', 1)
            logger.debug('Command: {}'.format(command))
            process = Popen(command[1], shell=True, stdout=PIPE, stderr=PIPE)
            stdout, stderr = process.communicate()
            if stdout:
                logger.debug('Command output: {}'.format(stdout))
                if len(stdout.decode('utf-8')) > 2048:
                    text = [stdout.decode('utf-8')[i:i + 2048] for i in range(0, len(stdout.decode('utf-8')), 2048)]
                    for i in text:
                        await message.reply(i)
                        await sleep(1)
                else:
                    await message.reply(stdout.decode('utf-8'))

            if stderr:
                logger.debug('Command error: {}'.format(stderr))
                if len(stderr.decode('utf-8')) > 2048:
                    text = [stderr.decode('utf-8')[i:i + 2048] for i in range(0, len(stderr.decode('utf-8')), 2048)]
                    for i in text:
                        await message.reply(i)
                        await sleep(1)
            logger.debug('Command {} from {} executed'.format(message.text, message.from_user.id))
        else:
            await message.reply('You are not admin')
        update_user_info(message)

    @bot_dp.message_handler(commands=['e', 'eval', 'е'])  # python eval
    async def evalpy(message: types.Message):
        logger.info('Command /eval from {}'.format(message.from_user.id))
        if check_user(message) == False:
            add_user(message)
        else:
            add_message(message)
        if check_superadmin(message.from_user.id) == True or check_admin(message) == True:
            command = message.text.split(' ', 1)[1]
            logger.debug('Command: {}'.format(command))
            try:
                await message.reply(eval(command))
            except Exception as e:
                await message.reply(e)