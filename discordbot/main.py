from DiscordBot import DiscordBot
from os import environ, listdir, path

discord_secret = environ.get('DISCORD_BOT_API')

discord_bot = DiscordBot('!')

for fileName in [".".join(f.split(".")[:-1]) for f in listdir('cogs') if path.isfile(path.join('cogs', f))]:
    print('Loading cog {0}'.format(fileName))
    discord_bot.load_extension('cogs.{0}'.format(fileName))

discord_bot.run(discord_secret)
