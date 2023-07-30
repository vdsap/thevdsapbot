from loguru import logger
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from datab import create_db
from conf_init import conf_init, tgclient_init
from commands.main_commands import commands
from commands.admin.console_admin_commands import terminal_commands as term_commands
from commands.admin.bot_inline_commands import inline_command as inline
from commands.public_commands import public as pub_commands
from commands.admin.bot_admin_commands import message_commands as admin_commands
import asyncio


# logger.level()

async def on_startup(dp):
    logger.info('Bot started')
    await bot.send_message(821461129, "Bot started",reply_markup=types.ReplyKeyboardRemove())


logger.info('Init bot')
conf = conf_init()
bot = Bot(token=conf['api_token'])
bot.parse_mode = "html"
storage = MemoryStorage()
tgclient = tgclient_init(conf)

dp = Dispatcher(bot, storage=storage)
logger.info('Init commands')
commands(dp)
term_commands(dp)
inline(bot, dp)
pub_commands(dp)
admin_commands(dp, bot, conf, tgclient)
create_db()

logger.info('Start bot')

if __name__ == '__main__':
    logger.info('Polling started')
    try:
        asyncio.run(executor.start_polling(dp, skip_updates=True, on_startup=on_startup))
    except Exception as err:
        logger.error(err)
