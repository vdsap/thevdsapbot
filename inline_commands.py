from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from loguru import logger
from datab import *
from asyncio import sleep
import random


# def inline_command(bot_dp):
#     @bot_dp.inline_handler()
#     async def inline(inline_query: InlineQuery):
#         logger.info('Command /inline from {}'.format(message.from_user.id))
#         if check_user(message) == False:
#             add_user(message)
#         else:
#             add_message(message)
#         if check_superadmin(message.from_user.id) == True or check_admin(message) == True:
#             item = InlineQueryResultArticle(
#                 id=random.randint(1, 1000),
#                 title='Evaluated',
#                 input_message_content=input_content
#             )
#             await bot.answer_inline_query(inline_query.id, results=[item], cache_time=1)
#         else:
#             await message.reply('You are not admin')
#         update_user_info(message)


def inline_command(bot, bot_dp):
    logger.info('Init Inline commands')
    @bot_dp.inline_handler()
    async def inline_eval(inline_query: InlineQuery):
        text = inline_query.query
        if text not in ['', ' ']:
            try: evaluated = eval(text)
            except Exception as e: evaluated = e
        else:
            evaluated = 'Nothing to evaluate'
        item = InlineQueryResultArticle(
            id=str(random.randint(1, 1000)),
            title=f'Result: {evaluated}',
            input_message_content=InputTextMessageContent(f'Evaluated:\n{text}\nReturn value:\n{evaluated}'),
        )
        logger.debug('Inline query: {}'.format(text))
        await bot.answer_inline_query(inline_query.id, results=[item], cache_time=1)


    # async def evalpy(message: types.Message):
    #     logger.info('Command /eval from {}'.format(message.from_user.id))
    #     if check_user(message) == False:
    #         add_user(message)
    #     else:
    #         add_message(message)
    #     if check_superadmin(message.from_user.id) == True or check_admin(message) == True:
    #         command = message.text.split(' ', 1)
    #         logger.debug('Command: {}'.format(command))
    #         try:
    #             await message.reply(eval(command))
    #         except Exception as e:
    #             await message.reply(e)