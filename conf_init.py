from yaml import safe_load as load
from loguru import logger
from telethon import TelegramClient

def conf_init():
    with open('conf.yaml') as f:
        logger.debug('Loading config')
        return load(f)

def check_superadmin(user_id: int):
    logger.debug('Checking superadmin status for {}'.format(user_id))
    conf = conf_init()
    if user_id in conf['superadmin']:
        logger.debug('{} is superadmin'.format(user_id))
        return True
    else:
        logger.debug('{} is not superadmin'.format(user_id))
        return False

def tgclient_init(config):
    logger.debug('Signing in user')
    client = TelegramClient(config['client_name'], config['api_id'], config['api_hash'], app_version='1.0',
                            device_model='thevdsapbot')
    return client