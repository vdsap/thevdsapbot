class TgLogger:
    bot = None
    LogsQueue = []
    RangeLoggPush = 10
    Chat_ID = -1002222067956

    def __init__(self, bot):
        TgLogger.bot = bot

    async def receiving_method(self, record):
        text = record
        text = f"""{text.split(".")[0]}\n"""
        TgLogger.LogsQueue.append(text)

        if len(TgLogger.LogsQueue) >= TgLogger.RangeLoggPush:
            text = ""
            for i in range(TgLogger.RangeLoggPush):
                text += TgLogger.LogsQueue.pop(-1)
            await self.bot.send_message(TgLogger.Chat_ID, f"<pre>{text}</pre>")
