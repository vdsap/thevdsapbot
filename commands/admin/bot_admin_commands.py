import io

from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from loguru import logger
from subprocess import Popen, PIPE
from datab import *
from telethon_client import tgsendmes
from typing import BinaryIO

def message_commands(dp,bot,conf,tgclient):
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

    @dp.message_handler(commands=['t', 'terminal', 'т'])  # Terminal
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
                        await message.reply(f'<code>{i}</code>')
                        await sleep(1)
                else:
                    await message.reply(f"""<code>{stdout.decode('utf-8')}</code>""")
            if stderr:
                logger.debug('Command error: {}'.format(stderr))
                if len(stderr.decode('utf-8')) > 2048:
                    text = [stderr.decode('utf-8')[i:i + 2048] for i in range(0, len(stderr.decode('utf-8')), 2048)]
                    for i in text:
                        await message.reply(f'<code>{i}</code>')
                        await sleep(1)
            else:
                await message.reply("Nothing to answer")
        else:
            await message.reply('You are not admin')
        logger.debug('Command {} from {} executed'.format(message.text, message.from_user.id))
        update_user_info(message)

    @dp.message_handler(commands=['e', 'eval', 'е'])  # python eval
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


    class Samokat_state(StatesGroup):
        text_from_user = State()
        photo = State()

    @dp.message_handler(commands=['samokat'])  # отдать смену в самокате
    async def samokat(message: types.Message):
        logger.info('Command /samokat from {}'.format(message.from_user.id))
        if check_user(message) == False:
            add_user(message)
        else:
            add_message(message)
        if (check_superadmin(message.from_user.id) == True or check_admin(message) == True) and message.from_user.id == 821461129:
            await Samokat_state.text_from_user.set()
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True,one_time_keyboard=True)
            markup.add("cancel")
            await bot.send_message(message.from_user.id,'Пришли сообщение в стиле:\n Дата смены\n Часы смены\n ФИО курьера',reply_markup=markup)
            logger.debug('Message samokat sent')

    @dp.message_handler(state='*', commands='cancel')
    @dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
    async def cancel_handler(message: types.Message, state: FSMContext):
        current_state = await state.get_state()
        if current_state is None:
            return
        logger.info(f'Cancelling state {current_state}')
        await state.finish()
        await message.reply('Cancelled.',reply_markup=types.ReplyKeyboardRemove())

    @dp.message_handler(state=Samokat_state.text_from_user)
    async def process_name(message: types.Message, state: FSMContext):
        """
        Process text from user
        """
        async with state.proxy() as data:
            data['text_from_user'] = message.text

        await Samokat_state.photo.set()
        await bot.send_message(message.from_user.id,'Пришли скриншот переписки')
        logger.info('Text_from_user got')

    @dp.message_handler(state=Samokat_state.photo,content_types=['photo'])
    async def process_name(message: types.Message, state: FSMContext):
        logger.debug('photo got')
        async with state.proxy() as data:
            data["photo"] = message.photo[-1]
            file_id = data["photo"].file_id
            file = await bot.get_file(file_id)
            file_path = file.file_path
            photo_bytes = await bot.download_file(file_path)
            logger.debug('Photo got')
            logger.info('Proccesing infos')
            text_from_user = data["text_from_user"].split('\n')
            text_temp = text_from_user[1].split('-')
            text_from_user[1] = f'{text_temp[0]}:00 - {text_temp[1]}:00'
            text1= f"/start,3,4,1,2,{text_from_user[0]},{text_from_user[1]}\n{text_from_user[2]}"
            text2= f"""{conf['my_fio']},{conf['my_number']},1""".split(',')
            final_text1 = text1.split(',')
            logger.info("Sending messages")
            result = await tgsendmes(tgclient,final_text1,photo_bytes,text2)
            if result == None:
                logger.debug('Completed')
                await bot.send_message(message.from_user.id,'Completed',reply_markup=types.ReplyKeyboardRemove())
            else:
                await bot.send_message(message.from_user.id, result, reply_markup=types.ReplyKeyboardRemove())
        await state.finish()