from discord.ext import commands
from helpers.roles import DiscordRoles


class DcsMissionCog(commands.Cog):
    weatherPresets = ['Preset{0}'.format(num) for num in range(1, 28)]

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role(DiscordRoles.DCSServerAdministrator)
    async def set_weather_preset(self, ctx, *, preset):
        if not preset:
            await ctx.send("Invalid preset specified")
            return

        if preset not in self.weatherPresets:
            await ctx.send('{0} is not a valid preset selection.'.format(preset))
            await ctx.send('Valid selections are {0}'.format(', '.join(self.weatherPresets)))
            return

        await ctx.send('Setting weather preset to {0}'.format(preset))


def setup(bot):
    bot.add_cog(DcsMissionCog(bot))