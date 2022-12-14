import discord
from discord.ext import commands

from helpers import DcsServerRepository, DcsMissionEditor
from helpers.services import dcs_server_repository, open_weather_map_service
from weather import CityNotFoundError, OpenMapWeatherService


class DcsMissionCog(commands.Cog, name="DCS Mission Commands"):
    def __init__(self,
                 bot,
                 weather_service: OpenMapWeatherService,
                 dcs_server: DcsServerRepository):
        self.bot = bot
        self.weather_service: OpenMapWeatherService = weather_service
        self.dcs_server: DcsServerRepository = dcs_server

    @commands.command(help="Sets the weather to that of a specified city.")
    async def set_weather(self, ctx, instance_name, *, city):
        if instance_name is None:
            await ctx.send('Command syntax: !set_weather <instance> <city>')
            return

        instance = self.dcs_server.get_instance(instance_name)
        if instance is None:
            await ctx.send(f'{instance} is not a valid instance.')
            return

        mission = instance.get_mission()

        try:
            weather = self.weather_service.get_weather_by_city(city)
        except CityNotFoundError:
            await ctx.send(f'"{city}" is not a valid city')
            return

        await ctx.send('Updating weather for the mission')

        dcs_mission = DcsMissionEditor(mission)
        weather_result = dcs_mission.set_weather(weather)

        instance.stop()
        dcs_mission.save()
        instance.start()

        embed = discord.Embed(title='Mission Weather Updated')\
            .set_thumbnail(url=f'http://openweathermap.org/img/w/{weather.info.icon}.png')\
            .add_field(name='Date', value=weather_result.time, inline=False)\
            .add_field(name='Clouds', value=weather_result.preset_name)\
            .add_field(name='Clouds Base', value='{:,}ft'.format(weather_result.cloud_base))\
            .add_field(name='Temperature', value=f'{weather_result.temperature}°C')\
            .add_field(name='Pressure', value="{:.2f}inHg".format(weather_result.pressure.value))\
            .add_field(name='Wind at Ground', value=f'{weather_result.wind_at_ground.speed}kts at {weather_result.wind_at_ground.direction}°')\
            .add_field(name='Wind at 2,000', value=f'{weather_result.wind_at_2000.speed}kts at {weather_result.wind_at_2000.direction}°')\
            .add_field(name='Wind at 8,000', value=f'{weather_result.wind_at_8000.speed}kts at {weather_result.wind_at_8000.direction}°')\

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(DcsMissionCog(bot,
                              open_weather_map_service,
                              dcs_server_repository))
