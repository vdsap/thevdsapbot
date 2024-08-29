from datab import *
from aiogram.types import InlineQuery, InlineQueryResultArticle, InputTextMessageContent
import random


def inline_command(bot, dp):
    logger.info('Init Inline commands')

    @dp.inline_handler()
    async def inline_eval(inline_query: InlineQuery):
        text = inline_query.query
        if not check_user(inline_query):
            add_user(inline_query)
        else:
            add_message(inline_query)
        if check_superadmin(inline_query.from_user.id) == True or check_admin(inline_query.from_user.id) == True:
            if text not in ['', ' ']:
                try:
                    code = compile(text, "<string>", "eval")
                    evaluated = eval(code)
                except Exception as e:
                    evaluated = e
            else:
                evaluated = 'Nothing to evaluate'
        else:
            evaluated = 'You are not allowed to use this function'
        item = InlineQueryResultArticle(
            id=str(random.randint(1, 1000)),
            title=f'Result: {evaluated}',
            input_message_content=InputTextMessageContent(f'Evaluated:\n{text}\nReturn value:\n{evaluated}'),
        )
        logger.debug('Inline query: {}'.format(text))
        logger.debug('Inline query result: {}'.format(evaluated))
        await bot.answer_inline_query(inline_query.id, results=[item])
        update_user_info(inline_query)
