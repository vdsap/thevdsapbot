from loguru import logger
from aiogram import Bot, Dispatcher, executor

from datab import create_db
from conf_init import conf_init
from commands.main_commands import commands
from commands.admin.console_admin_commands import terminal_commands as term_commands
from commands.admin.bot_inline_commands import inline_command as inline
from commands.public_commands import public as pub_commands
from commands.admin.bot_admin_commands import message_commands as admin_commands


# logger.level()

async def on_startup(dp):
    logger.info('Bot started')
    await bot.send_message(821461129, "Bot started")

logger.info('Init bot')
conf = conf_init()
bot = Bot(token=conf['api_token'])
bot.parse_mode = "html"

dp = Dispatcher(bot)
logger.info('Init commands')
commands(dp)
term_commands(dp)
inline(bot, dp)
pub_commands(dp)
admin_commands(dp)
create_db()

logger.info('Start bot')

if __name__ == '__main__':
    logger.info('Polling started')
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

