import discord
import asyncio
from redbot.core import commands, Config, checks
from datetime import datetime, timedelta, time


class Events(getattr(commands, "Cog", object)):
    """
    PoGo Events
    """

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1892027056)
        self.settings = Config.get_conf(None, identifier=602700309, cog_name="Info")
        self.auto_check = self.bot.loop.create_task(self.auto_worker())
        self.config.register_global(**{"nest": datetime.utcnow().timestamp()})

    def __unload(self):
        self.auto_check.cancel()

    @commands.command()
    async def events(self, ctx):
        """
        Show a list of active events
        """

        await ctx.send("hi")

    @commands.command()
    @checks.admin_or_permissions(manage_channel=True)
    async def nest(self, ctx):
        """
        Report an off-cycle Nest Migration
        """

        guild = ctx.guild
        chan = await self.settings.guild(guild).channel()
        if ctx.message.channel.id != chan["nest"]:
            return

        await ctx.message.delete()
        await ctx.send(
            "**ATTENTION TRAINERS!!** We are getting reports of a surprise Nest Migration.\n"
            "Please treat any of the nest reports above as out-dated until confirmed.\n"
            "\n"
            "As always, please assist your fellow trainers by reporting the new nesting species at <https://thesilphroad.com/atlas> in addition to this channel\n"
            "\n"
            "Travel safe Trainers"
        )

    async def auto_worker(self):
        """
        Handles automated postings/deletions
        """

        while self == self.bot.get_cog("Events"):
            for guild in self.bot.guilds:
                channel = await self.settings.guild(guild).channel()
                nests = await self.config.nest()
                nest = datetime.utcfromtimestamp(nests)
                settings = await self.settings.guild(guild).settings()
                if channel is not None:
                    if channel["nest"] is not None and (190 > (datetime.utcnow() - nest).seconds):
                        await self.bot.get_channel(channel["nest"]).send(
                            "The next Great Global Nest Migration has taken place.\n"
                            "Please treat all previous nest reports above as out-dated unless reconfirmed below\n"
                            "As always, please assist your fellow trainers by reporting the new nesting species at <https://thesilphroad.com/atlas> in addition to this channel\n"
                            "Travel safe Trainers"
                        )
                        await self.config.nest.set((nest + timedelta(days=14)).timestamp())

                    if channel["research"] is not None and (
                        datetime.utcnow() + timedelta(hours=settings["tz"])
                    ).time().replace(microseconds=0) == time(0, 0, 0):
                        history = await self.bot.get_channel(channel["research"]).history(
                            after=(datetime.utcnow() - timedelta(days=1))
                        )
                        async for hist in history:
                            await hist.delete()

            await asyncio.sleep(60)
