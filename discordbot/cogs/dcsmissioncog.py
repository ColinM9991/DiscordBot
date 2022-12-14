import dcs
from dcs.weather import CloudPreset
from discord.ext import commands
from os import environ

from helpers import DiscordRoles, OpenMapWeatherService, CityNotFoundError, DcsWeatherMapper
from helpers.dcsmissioneditor import DcsMissionEditor


class DcsMissionCog(commands.Cog, name="DCS Mission Commands"):
    weatherPresets = [f'Preset{num}' for num in range(1, 28)]

    def __init__(self, bot, weather_service, dcs_weather_mapper):
        self.bot = bot
        self.weather_service = weather_service
        self.dcs_weather_mapper = dcs_weather_mapper

    @commands.command(help="Sets the clouds preset for the mission.")
    @commands.has_role(DiscordRoles.DCSServerAdministrator)
    async def set_clouds_preset(self, ctx, preset):
        if preset not in self.weatherPresets:
            await ctx.send(f'{preset} is not a valid preset selection.')
            await ctx.send('Valid selections are {0}'.format(', '.join(self.weatherPresets)))
            return

        await ctx.send('Setting weather preset to {0}'.format(preset))

    @commands.command(help="Sets the weather to that of the specified city.")
    async def set_weather(self, ctx, *, city):
        try:
            weather = self.weather_service.get_weather_by_city(city)
        except CityNotFoundError:
            await ctx.send(f'"{city}" is not a valid city')
            return

        dcs_weather = self.dcs_weather_mapper.map(weather)

        mission_file = 'blank'
        dcs_mission = DcsMissionEditor(mission_file)
        weather_result = dcs_mission.set_weather(dcs_weather)
        dcs_mission.save()

        await ctx.send(f'Weather set to {weather_result.preset_name} with a pressure of {weather_result.pressure}')


def setup(bot):
    bot.add_cog(DcsMissionCog(bot,
                              OpenMapWeatherService(
                                  environ.get('DISCORD_OPEN_WEATHER_MAP_URL'),
                                  environ.get('DISCORD_OPEN_WEATHER_MAP_API_KEY')),
                              DcsWeatherMapper()))
