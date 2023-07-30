from asyncio import sleep
from loguru import logger


async def tgsendmes(client, text1, photo, text2):
    async with client:
        logger.debug('Sending texts')
        for text in text1:
            await client.send_message('SamokatInternalSupportBot', text)
            await sleep(1)
        logger.info('Texts sent')
        await sleep(1)
        logger.debug('Sending photo')
        await client.send_file('SamokatInternalSupportBot', photo)
        await sleep(1)
        for txt in text2:
            await client.send_message('SamokatInternalSupportBot', txt)
            await sleep(1)
