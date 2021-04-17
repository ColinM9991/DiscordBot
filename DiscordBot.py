from discord.ext import commands


class DiscordBot(commands.Bot):
    def __init__(self, command_prefix):
        super().__init__(command_prefix)

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))
        await super().on_message(message)