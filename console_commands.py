from aiogram import types
from loguru import logger
from datab import *
from subprocess import Popen, PIPE
import io
import urllib.request as request
from asyncio import sleep

def terminal_commands(bot_dp):
    logger.info('Init terminal commands')
    @bot_dp.message_handler(commands=['t','terminal','т'])                                           # Terminal
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
                if len (stdout.decode('utf-8')) > 2048:
                    text = [stdout.decode('utf-8')[i:i+2048] for i in range(0, len(stdout.decode('utf-8')), 2048)]
                    for i in text:
                        await message.reply(i)
                        await sleep(1)
                else:
                    await message.reply(stdout.decode('utf-8'))

            if stderr:
                logger.debug('Command error: {}'.format(stderr))
                if len (stderr.decode('utf-8')) > 2048:
                    text = [stderr.decode('utf-8')[i:i+2048] for i in range(0, len(stderr.decode('utf-8')), 2048)]
                    for i in text:
                        await message.reply(i)
                        await sleep(1)
            logger.debug('Command {} from {} executed'.format(message.text, message.from_user.id))
        else:
            await message.reply('You are not admin')
        update_user_info(message)


    @bot_dp.message_handler(commands=['e','eval','е'])                                          # python eval
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


    @bot_dp.message_handler(commands=['wg_reboot'])                                           # reboot wg
    async def wg_reboot(message: types.Message):
        logger.info('Command /wg_reboot from {}'.format(message.from_user.id))
        if check_user(message) == False:
            add_user(message)
        else:
            add_message(message)
        if check_superadmin(message.from_user.id) == True or check_admin(message) == True:
            process = Popen('systemctl restart wg-quick@wg_broadwell', shell=True, stdout=PIPE, stderr=PIPE)
            stdout, stderr = process.communicate()
            if stderr:
                logger.debug('Command error: {}'.format(stderr))
                if len (stderr.decode('utf-8')) > 2048:
                    text = [stderr.decode('utf-8')[i:i+2048] for i in range(0, len(stderr.decode('utf-8')), 2048)]
                    for i in text:
                        await message.reply(i)
                        await sleep(1)
                else:
                    await message.reply(stderr.decode('utf-8'))
            await message.reply('Wireguard rebooted')
            logger.debug('Wireguard rebooted')
            await sleep(1)
            process = Popen('wg', shell=True, stdout=PIPE, stderr=PIPE)
            stdout, stderr = process.communicate()
            await message.reply(stdout.decode('utf-8'))
        else:
            await message.reply('You are not admin')
        update_user_info(message)


    @bot_dp.message_handler(commands=['wg_stat'])                                           # wg status
    async def wg_status(message: types.Message):
        logger.info('Command /wg_status from {}'.format(message.from_user.id))
        if check_user(message) == False:
            add_user(message)
        else:
            add_message(message)
        if check_superadmin(message.from_user.id) == True or check_admin(message) == True:
            process = Popen('wg', shell=True, stdout=PIPE, stderr=PIPE)
            stdout, stderr = process.communicate()
            if stderr:
                logger.debug('Command error: {}'.format(stderr))
                if len (stderr.decode('utf-8')) > 2048:
                    text = [stderr.decode('utf-8')[i:i+2048] for i in range(0, len(stderr.decode('utf-8')), 2048)]
                    for i in text:
                        await message.reply(i)
                        await sleep(1)
                else:
                    await message.reply(stderr.decode('utf-8'))
            await message.reply(stdout.decode('utf-8'))
        else:
            await message.reply('You are not admin')
        update_user_info(message)


    @bot_dp.message_handler(commands=['reboot'])                                           # reboot bot
    async def reboot(message: types.Message):
        logger.info('Command /reboot from {}'.format(message.from_user.id))
        if check_user(message) == False:
            add_user(message)
        else:
            add_message(message)
        if check_superadmin(message.from_user.id) == True:
            await message.reply('Rebooting...')
            process = Popen('systemctl restart thevdsapbot', shell=True, stdout=PIPE, stderr=PIPE)
            stdout, stderr = process.communicate()
            if stderr:
                logger.debug('Command error: {}'.format(stderr))
                if len (stderr.decode('utf-8')) > 2048:
                    text = [stderr.decode('utf-8')[i:i+2048] for i in range(0, len(stderr.decode('utf-8')), 2048)]
                    for i in text:
                        await message.reply(i)
                        await sleep(1)
                else:
                    await message.reply(stderr.decode('utf-8'))
            await message.reply('Bot rebooted')
            logger.debug('Bot rebooted')
        else:
            await message.reply('You are not admin')
        update_user_info(message)


    @bot_dp.message_handler(commands=['update'])                                        # update bot
    async def update(message: types.Message):
        logger.info('Command /update from {}'.format(message.from_user.id))
        if check_user(message) == False:
            add_user(message)
        else:
            add_message(message)
        if check_superadmin(message.from_user.id) == True:
            await message.reply('Updating...')
            process = Popen('git pull', shell=True, stdout=PIPE, stderr=PIPE)
            stdout, stderr = process.communicate()
            if stderr:
                logger.debug('Command error: {}'.format(stderr))
                if len (stderr.decode('utf-8')) > 2048:
                    text = [stderr.decode('utf-8')[i:i+2048] for i in range(0, len(stderr.decode('utf-8')), 2048)]
                    for i in text:
                        await message.reply(i)
                        await sleep(1)
                else:
                    await message.reply(stderr.decode('utf-8'))
            await message.reply('Bot updated')
            logger.debug('Bot updated')
            Popen('systemctl restart thevdsapbot', shell=True, stdout=PIPE, stderr=PIPE)
        else:
            await message.reply('You are not admin')
        update_user_info(message)


    @bot_dp.message_handler(commands=['start_qbittorrent'])                                            # start qbittorrent
    async def start_qbittorrent(message: types.Message):
        logger.info('Command /start_qbittorrent from {}'.format(message.from_user.id))
        if check_user(message) == False:
            add_user(message)
        else:
            add_message(message)
        if check_superadmin(message.from_user.id) == True or check_admin(message) == True:
            process = Popen('systemctl start qbittorrent.service', shell=True, stdout=PIPE, stderr=PIPE)
            stdout, stderr = process.communicate()
            if stderr:
                logger.debug('Command error: {}'.format(stderr))
                if len (stderr.decode('utf-8')) > 2048:
                    text = [stderr.decode('utf-8')[i:i+2048] for i in range(0, len(stderr.decode('utf-8')), 2048)]
                    for i in text:
                        await message.reply(i)
                        await sleep(1)
                else:
                    await message.reply(stderr.decode('utf-8'))
            await message.reply('Qbittorrent started')
            logger.debug('Qbittorrent started')
        else:
            await message.reply('You are not admin')
        update_user_info(message)

    @bot_dp.message_handler(commands=['stop_qbittorrent'])                                            # stop qbittorrent
    async def stop_qbittorrent(message: types.Message):
        logger.info('Command /stop_qbittorrent from {}'.format(message.from_user.id))
        if check_user(message) == False:
            add_user(message)
        else:
            add_message(message)
        if check_superadmin(message.from_user.id) == True or check_admin(message) == True:
            process = Popen('systemctl stop qbittorrent.service', shell=True, stdout=PIPE, stderr=PIPE)
            stdout, stderr = process.communicate()
            if stderr:
                logger.debug('Command error: {}'.format(stderr))
                if len (stderr.decode('utf-8')) > 2048:
                    text = [stderr.decode('utf-8')[i:i+2048] for i in range(0, len(stderr.decode('utf-8')), 2048)]
                    for i in text:
                        await message.reply(i)
                        await sleep(1)
                else:
                    await message.reply(stderr.decode('utf-8'))
            await message.reply('Qbittorrent stopped')
            logger.debug('Qbittorrent stopped')
        else:
            await message.reply('You are not admin')
        update_user_info(message)