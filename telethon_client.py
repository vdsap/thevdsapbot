from asyncio import sleep
from loguru import logger

contact = 'SamokatInternalSupportBot'
# contact = 950545630 # GasPlita
async def tgsendmes(client, text1, photo, text2):
    async with client:
        logger.debug('Sending texts')
        for text in text1:
            await client.send_message(contact, text)
            await sleep(1)
        logger.info('Texts sent')
        await sleep(1)
        logger.debug('Sending photo')
        await client.send_file(contact, photo)
        await sleep(1)
        for txt in text2:
            await client.send_message(contact, txt)
            await sleep(1)
