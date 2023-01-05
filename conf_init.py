from yaml import safe_load as load
from loguru import logger

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
