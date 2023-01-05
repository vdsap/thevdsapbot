from datab import *
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent


def inline_command(bot, dp):
    logger.info('Init Inline commands')
    @dp.inline_handler()
    async def inline_eval(inline_query: InlineQuery):
        qu = inline_query
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