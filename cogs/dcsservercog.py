from discord.ext import commands
from DcsServer import DcsServer
from helpers.roles import DiscordRoles


class DcsServerCog(commands.Cog):
    def __init__(self, bot, dcs_server: DcsServer):
        self.bot = bot
        self.dcs_server = dcs_server

    @commands.command()
    @commands.has_role(DiscordRoles.DCSServerAdministrator)
    async def restart_server(self, ctx):
        await ctx.send("{0} {1} {2}")

    @commands.command()
    async def check_server(self, ctx):
        if self.dcs_server.is_running():
            await ctx.send('The server is currently running')
        else:
            await ctx.send('The server is currently offline')


def setup(bot):
    bot.add_cog(DcsServerCog(bot, DcsServer()))