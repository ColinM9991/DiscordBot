import discord
from discord.ext import commands

from helpers import DcsServerRepository
from helpers.services import dcs_server_repository


class DcsServerCog(commands.Cog, name='DCS Server Commands'):
    def __init__(self, bot, dcs_server: DcsServerRepository):
        self.bot = bot
        self.dcs_server: DcsServerRepository = dcs_server

    @commands.command(help='Retrieves the server information for a given instance')
    async def server_info(self, ctx, instance=None):
        if instance is not None:
            await self.get_server_info(ctx, instance)
        else:
            for instance_name in self.dcs_server.get_instance_names():
                await self.get_server_info(ctx, instance_name)

    @commands.command(help='Returns the instance names all DCS Servers.')
    async def get_instances(self, ctx):
        instances = self.dcs_server.get_instance_names()

        await ctx.send(f'Available instances are {", ".join(instances)}')

    async def get_server_instance(self, ctx, instance):
        try:
            dcs_instance = self.dcs_server.get_instance(instance)
        except ValueError:
            await ctx.send('Invalid instance specified')
            raise

        return dcs_instance

    async def get_server_info(self, ctx, instance):
        dcs_instance = await self.get_server_instance(ctx, instance)

        server_info = dcs_instance.get_server_info()

        embed = discord.Embed(title='DCS Server Information')\
            .add_field(name='Name', value=server_info.server_name, inline=False)\
            .add_field(name='IP', value=server_info.ip_address, inline=True)\
            .add_field(name='Port', value=server_info.port, inline=True)\
            .add_field(name='Status', value=('Online' if server_info.is_active else 'Offline'), inline=True)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(DcsServerCog(bot, dcs_server_repository))
