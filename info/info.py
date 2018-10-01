import discord
from redbot.core import commands, __version__
import sys


class Info:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="info", aliases=["about"])
    async def _info(self, ctx):
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
        embed.add_field(name="Data Sources", value="Unknown", inline=False)
        embed.add_field(name="Owner", value=str(owner), inline=True)
        embed.add_field(name="Python", value=python_version, inline=True)
        embed.add_field(name="discord.py", value=dpy_version, inline=True)
        embed.add_field(name="Red", value=red_version, inline=True)
        await ctx.send(embed=embed)
