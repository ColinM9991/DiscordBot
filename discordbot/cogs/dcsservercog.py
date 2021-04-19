from discord.ext import commands
from helpers.dcsserver import ConcreteDcsServer


class DcsServerCog(commands.Cog, name="DCS Server Commands"):
    def __init__(self, bot, dcs_server):
        self.bot = bot
        self.dcs_server = dcs_server

    @commands.command(help="Checks the status of the DCS server.")
    async def check_server(self, ctx):
        if self.dcs_server.is_running():
            await ctx.send('The server is currently running')
        else:
            await ctx.send('The server is currently offline')


def setup(bot):
    bot.add_cog(DcsServerCog(bot, ConcreteDcsServer()))
