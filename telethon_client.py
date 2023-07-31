from asyncio.exceptions import TimeoutError
from loguru import logger

# contact = 'SamokatInternalSupportBot'


contact = 950545630 # GasPlita
async def tgsendmes(client, text1, photo, text2):
    await client.connect()
    await client.start()

    async with client.conversation(contact) as conv:
        logger.debug('Sending texts')
        for txt1 in text1:
            logger.debug(f'Sending: {txt1}')
            await conv.send_message(txt1)
            try:
                await conv.get_response(timeout=600)
            except TimeoutError:
                logger.error("Бот самоката мертв")
                return "Samokat bot dead"
        logger.info('Texts sent')
        logger.debug('Sending photo')
        await conv.send_file(photo)
        try:
            await conv.get_response(timeout=600)
        except TimeoutError:
            logger.error("Бот самоката мертв")
            return "Samokat bot dead"
        for txt2 in text2:
            logger.debug(f'Sending: {txt2}')
            await conv.send_message(txt2)
            try:
                await conv.get_response(timeout=600)
            except TimeoutError:
                logger.error("Бот самоката мертв")
                return "Samokat bot dead"
    logger.debug('Messages sent')
    await client.disconnect()
    return
