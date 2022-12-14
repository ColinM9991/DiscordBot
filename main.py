from DiscordBot import DiscordBot
import os

discord_secret = os.environ.get('DISCORD_BOT_API')

discord_bot = DiscordBot('!')

for fileName in [".".join(f.split(".")[:-1]) for f in os.listdir('cogs') if os.path.isfile(os.path.join('cogs', f))]:
    print('Loading cog {0}'.format(fileName))
    discord_bot.load_extension('cogs.{0}'.format(fileName))

discord_bot.run(discord_secret)