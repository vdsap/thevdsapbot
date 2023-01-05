from loguru import logger

from aiogram import Bot, Dispatcher, executor, types

from bot_commands import commands
from console_commands import terminal_commands as t_commands
from datab import create_db
from conf_init import conf_init
from inline_commands import inline_command as inline

# logger.level()

logger.info('Init bot')
conf = conf_init()
bot = Bot(token=conf['api_token'])
bot.parse_mode = "html"
bot_dp = Dispatcher(bot)

logger.info('Init commands')
commands(bot_dp)
t_commands(bot_dp)
inline(bot, bot_dp)
create_db()
logger.info('Start bot')

async def on_startup(bot_dp):
    logger.info('Bot started')
    await bot.send_message(821461129, "Bot started")

if __name__ == '__main__':
    logger.info('Polling started')
    executor.start_polling(bot_dp, skip_updates=True, on_startup=on_startup)

