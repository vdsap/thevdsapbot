from aiogram import types

from loguru import logger
from datab import *
from subprocess import Popen, PIPE

from asyncio import sleep
import random


def terminal_commands(bot_dp):
    logger.info('Init terminal commands')
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

    @bot_dp.message_handler(commands=['update_site'])  # update vdsaphtml
    async def update(message: types.Message):
        logger.info('Command /update_site from {}'.format(message.from_user.id))
        if check_user(message) == False:
            add_user(message)
        else:
            add_message(message)
        if check_superadmin(message.from_user.id) == True:
            await message.reply('Updating site...')
            process = Popen('cd /main/vdsaphtml && git pull', shell=True, stdout=PIPE, stderr=PIPE)
            stdout, stderr = process.communicate()
            if stderr:
                logger.debug('Command error: {}'.format(stderr))
                if len(stderr.decode('utf-8')) > 2048:
                    text = [stderr.decode('utf-8')[i:i + 2048] for i in range(0, len(stderr.decode('utf-8')), 2048)]
                    for i in text:
                        await message.reply(i)
                        await sleep(1)
                else:
                    await message.reply(stderr.decode('utf-8'))
            await message.reply('Vdsaphtml updated')
            logger.debug('Vdsaphtml updated')
            Popen('systemctl restart nginx', shell=True, stdout=PIPE, stderr=PIPE)
        else:
            await message.reply('You are not admin')
        update_user_info(message)