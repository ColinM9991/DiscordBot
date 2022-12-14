from discord.ext import commands
from helpers.dcsserver import ConcreteDcsServer, DcsServer
from os import environ


class DcsServerCog(commands.Cog, name="DCS Server Commands"):
    def __init__(self, bot, dcs_server: DcsServer):
        self.bot = bot
        self.dcs_server: DcsServer = dcs_server

    @commands.command(help="Checks the status of the DCS server.")
    async def check_server(self, ctx):
        if self.dcs_server.is_running():
            await ctx.send('The server is currently running')
        else:
            await ctx.send('The server is currently offline')

    @commands.command(help='Returns a list of registered instances.')
    async def get_instances(self, ctx):
        instances = self.dcs_server.get_instances()

        await ctx.send(f'Available instances are {", ".join(instances)}')


def setup(bot):
    bot.add_cog(DcsServerCog(bot, ConcreteDcsServer(environ.get('DCS_PROFILE_PATH'))))
