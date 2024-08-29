
class TgLogger:
    bot = None
    LogsQueue = []
    CountLogsSend = 0
    conf = None
    Chat_ID = 0

    def __init__(self, bot, conf):
        TgLogger.bot = bot
        TgLogger.conf = conf
        TgLogger.Chat_ID = TgLogger.conf["logs_chatid"]
        TgLogger.CountLogsSend = TgLogger.conf["count_logs_send"]

    async def receiving_method(self, record):
        text = record
        text = f"""{text.split(".")[0]}\n"""
        TgLogger.LogsQueue.append(text)

        if len(TgLogger.LogsQueue) >= TgLogger.CountLogsSend:
            print(TgLogger.LogsQueue)
            text = ""
            for i in range(TgLogger.CountLogsSend):
                text += TgLogger.LogsQueue.pop(-1)
            await self.bot.send_message(TgLogger.Chat_ID, f"<pre>{text}</pre>")
