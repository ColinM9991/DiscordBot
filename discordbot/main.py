import os

from discord.ext.commands import Bot

discord_secret = os.environ.get('DISCORD_BOT_API')

discord_bot = Bot(command_prefix='!')

for fileName in [".".join(f.split(".")[:-1]) for f in os.listdir('cogs') if os.path.isfile(os.path.join('cogs', f))]:
    print('Loading cog {0}'.format(fileName))
    discord_bot.load_extension('cogs.{0}'.format(fileName))

discord_bot.run(discord_secret)
