from discord.ext import commands
from helpers import DcsServerRepository

from helpers.services import dcs_server_repository


class DcsServerCog(commands.Cog, name="DCS Server Commands"):
    def __init__(self, bot, dcs_server: DcsServerRepository):
        self.bot = bot
        self.dcs_server: DcsServerRepository = dcs_server

    @commands.command(help="Checks the status of the DCS server.")
    async def check_server(self, ctx, instance):
        try:
            dcs_instance = self.dcs_server.get_instance(instance)
        except ValueError:
            await ctx.send('Invalid instance specified')
            raise

        if dcs_instance.is_running():
            await ctx.send(f'The {dcs_instance.get_instance_name} server is currently running')
        else:
            await ctx.send(f'The {dcs_instance.get_instance_name} server is currently offline')

    @commands.command(help='Returns the instance names all running DCS Servers.')
    async def get_instances(self, ctx):
        instances = self.dcs_server.get_instances()

        await ctx.send(f'Available instances are {", ".join(instances)}')


def setup(bot):
    bot.add_cog(DcsServerCog(bot, dcs_server_repository))
