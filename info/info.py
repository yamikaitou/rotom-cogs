import discord
from redbot.core import commands, __version__, checks, Config
import sys
from typing import Union


class Info(getattr(commands, "Cog", object)):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=602700309)
        default_guild = {
            "channel": {
                "role": None,
                "ex": None,
                "raid": None,
                "social": None,
                "research": None,
                "nest": None,
            },
            "setting": {"egg": None, "boss": None, "tz": None},
        }
        self.config.register_guild(**default_guild)

    @commands.command(name="about")
    async def _about(self, ctx):
        """
        Displays Info about Rotom
        """
        red_pypi = "https://pypi.python.org/pypi/Red-DiscordBot"
        dpy_repo = "https://github.com/Rapptz/discord.py"
        python_url = "https://www.python.org/"
        dpy_version = "[{}]({})".format(discord.__version__, dpy_repo)
        red_version = "[{}]({})".format(__version__, red_pypi)
        python_version = "[{}.{}.{}]({})".format(*sys.version_info[:3], python_url)
        app_info = await self.bot.application_info()
        owner = app_info.owner

        meowth_author = "https://github.com/FoglyOgly"
        red_author = "https://github.com/Twentysix26"
        org_author = "https://github.com/Cog-Creators"
        meowth_repo = "https://github.com/FoglyOgly/Meowth"
        red_repo = org_author + "/Red-DiscordBot"

        self_repo = "https://github.com/yamikaitou/rotom-cogs"
        self_author = "https://github.com/yamikaitou"

        embed = discord.Embed(
            description="Hi, I'm Rotom! Zzzt! I'm a Pokemon Go Discord Bot!\n\n"
            "I'm made by YamiKaitou to help manage a local Discord group.\n"
            "I'm based on functions/ideas from Meowth and build upon Red-DiscordBot.\n"
            "While I am open-source, I am specifically coded for a specific community."
        )
        embed.set_thumbnail(
            url="https://archives.bulbagarden.net/media/upload/3/36/479Rotom-Pok%C3%A9dex.png"
        )
        embed.add_field(
            name="Credits",
            value="[Meowth]({}): [FoglyOgly]({}) and many others\n"
            "[Red-DiscordBot]({}): [Twentysix]({}) and [many others]({})\n"
            "[Rotom]({}): [YamiKaitou]({})".format(
                meowth_repo,
                meowth_author,
                red_repo,
                red_author,
                org_author,
                self_repo,
                self_author,
            ),
            inline=False,
        )
        embed.add_field(
            name="Data Sources",
            value="[The Silph Road](https://thesilphroad.com/)\n[Serebii](https://www.serebii.net/)\n[Pokemon Go Hub](https://pokemongohub.net/)\n[Ranked Boost: Pokemon Go](https://rankedboost.com/category/pokemon-go/)",
            inline=False,
        )
        embed.add_field(name="Owner", value=str(owner), inline=True)
        embed.add_field(name="Python", value=python_version, inline=True)
        embed.add_field(name="discord.py", value=dpy_version, inline=True)
        embed.add_field(name="Red", value=red_version, inline=True)
        await ctx.send(embed=embed)

    @commands.group()
    @commands.guild_only()
    @checks.admin_or_permissions(manage_server=True)
    async def pogo(self, ctx):
        """
        Set various settings
        """
        if ctx.invoked_subcommand is None:
            guild = ctx.guild
            crole = await self.config.guild(guild).channel.role()
            cex = await self.config.guild(guild).channel.ex()
            craid = await self.config.guild(guild).channel.raid()
            csocial = await self.config.guild(guild).channel.social()
            cresearch = await self.config.guild(guild).channel.research()
            cnest = await self.config.guild(guild).channel.nest()
            segg = await self.config.guild(guild).setting.egg()
            sboss = await self.config.guild(guild).setting.boss()
            stz = await self.config.guild(guild).setting.tz()

            await ctx.send(
                "```"
                "Channel Locations\n"
                "Role Assign: {}\n"
                "EX Raids: {}\n"
                "Raids: {}\n"
                "Social Media: {}\n"
                "Research: {}\n"
                "Nests: {}\n"
                "\n"
                "Various Settings\n"
                "Raid Egg Timer: {}\n"
                "Raid Boss Timer: {}\n"
                "Timezone Offset: {}\n"
                "```".format(
                    guild.get_channel(crole),
                    guild.get_channel(cex),
                    guild.get_channel(craid),
                    guild.get_channel(csocial),
                    guild.get_channel(cresearch),
                    guild.get_channel(cnest),
                    segg,
                    sboss,
                    stz,
                )
            )

        pass

    @pogo.command()
    @commands.guild_only()
    async def role(self, ctx, channel: discord.TextChannel = None):
        """
        Set the channel for Role Assignment posts
        """
        if channel is None:
            await self.config.guild(ctx.guild).channel.role.set(ctx.channel.id)
        else:
            await self.config.guild(ctx.guild).channel.role.set(channel.id)

    @pogo.command()
    @commands.guild_only()
    async def ex(self, ctx, channel: discord.TextChannel = None):
        """
        Set the channel for EX-Raid Pass posts
        """
        if channel is None:
            await self.config.guild(ctx.guild).channel.ex.set(ctx.channel.id)
        else:
            await self.config.guild(ctx.guild).channel.ex.set(channel.id)

    @pogo.command()
    @commands.guild_only()
    async def raids(self, ctx, channel: discord.TextChannel = None):
        """
        Set the channel for Raid Channel Creation posts
        """
        if channel is None:
            await self.config.guild(ctx.guild).channel.raid.set(ctx.channel.id)
        else:
            await self.config.guild(ctx.guild).channel.raid.set(channel.id)

    @pogo.command()
    @commands.guild_only()
    async def social(self, ctx, channel: discord.TextChannel = None):
        """
        Set the channel for Social Media Postings
        """
        if channel is None:
            await self.config.guild(ctx.guild).channel.social.set(ctx.channel.id)
        else:
            await self.config.guild(ctx.guild).channel.social.set(channel.id)

    @pogo.command()
    @commands.guild_only()
    async def research(self, ctx, channel: discord.TextChannel = None):
        """
        Set the channel for Field Research posts
        """
        if channel is None:
            await self.config.guild(ctx.guild).channel.research.set(ctx.channel.id)
        else:
            await self.config.guild(ctx.guild).channel.research.set(channel.id)

    @pogo.command()
    @commands.guild_only()
    async def nest(self, ctx, channel: discord.TextChannel = None):
        """
        Set the channel for Nest reports
        """
        if channel is None:
            await self.config.guild(ctx.guild).channel.nest.set(ctx.channel.id)
        else:
            await self.config.guild(ctx.guild).channel.nest.set(channel.id)

    @pogo.command()
    @commands.guild_only()
    async def egg(self, ctx, time):
        """
        Set the time for Raid Eggs (in minutes)
        """
        await self.config.guild(ctx.guild).setting.egg.set(time)

    @pogo.command()
    @commands.guild_only()
    async def boss(self, ctx, time):
        """
        Set the time for Raid Bosses (in minutes)
        """
        await self.config.guild(ctx.guild).setting.boss.set(time)

    @pogo.command()
    @commands.guild_only()
    async def tz(self, ctx, time):
        """
        Set the timezone offset
        """
        await self.config.guild(ctx.guild).setting.tz.set(time)
