import discord
import random
from redbot.core import commands
from redbot.core import Config


class Roles(getattr(commands, "Cog", object)):
    """
    Role Management
    """

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=772041520)
        self.settings = Config.get_conf(None, identifier=602700309, cog_name="Info")

    @commands.command()
    @commands.guild_only()
    async def role(self, ctx, rolename=None):
        """
        Adds a role to the user

        :param rolename: Role Name
        """

        guild = ctx.guild
        chan = await self.settings.guild(guild).channel()
        if ctx.message.channel.id != chan["role"]:
            return

        msg = None

        if rolename is not None:
            try:
                gen = await self.config.guild(guild).gen()
                pkm = await self.config.guild(guild).pkm()
                exr = await self.config.guild(guild).exr()

                if rolename not in gen and rolename not in pkm and rolename not in exr:
                    raise AttributeError("Invalid Role")

                role = discord.utils.get(ctx.guild.roles, name=rolename)
                if role not in ctx.author.roles:
                    await ctx.author.add_roles(role)
                    await ctx.send("I have given you the role")
                    return
                else:
                    await ctx.author.remove_roles(role)
                    await ctx.send("I have taken the role from you")
                    return
            except AttributeError:
                msg = "I could not find that role, please try again\n"

        embed = discord.Embed(
            title="Available Roles",
            color=discord.Color(random.randint(0x000000, 0xFFFFFF)),
            description="Select one of the roles below to be added/removed from your profile\n\n"
            "Example: !role raids-all\n\n",
        )

        value = ""
        async with self.config.guild(guild).gen() as vals:
            for val in vals:
                value = value + "\n" + val

        embed.add_field(name="Locations", value=value)

        value = ""
        async with self.config.guild(guild).pkm() as vals:
            for val in vals:
                value = value + "\n" + val

        embed.add_field(name="Pokemon", value=value)

        value = ""
        async with self.config.guild(guild).exr() as vals:
            for val in vals:
                value = value + "\n" + val

        embed.add_field(name="EX Locations", value=value)

        await ctx.send(content=msg, embed=embed)
