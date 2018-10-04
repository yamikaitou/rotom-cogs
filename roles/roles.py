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

    @commands.command()
    @commands.guild_only()
    async def role(self, ctx, rolename=None):
        """
        Adds a role to the user

        :param rolename: Role Name
        """

        if (
            ctx.message.channel.id != 460650422986735626
            or ctx.message.channel.id != 362798066199298049
        ):
            pass

        msg = None

        if rolename is not None:
            try:
                gen = await self.config.gen.all()
                pkm = await self.config.pkm.all()
                exr = await self.config.exr.all()

                if rolename not in gen or rolename not in pkm or rolename not in exr:
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
                msg = "I could not find that role, please try again"

        embed = discord.Embed(
            title="Available Roles",
            color=discord.Color(random.randint(0x000000, 0xFFFFFF)),
            description="Select one of the roles below to be added/removed from your profile\n\n"
            "Example: !role raids-all\n\n",
        )

        value = ""
        async with self.config.gen() as vals:
            for val in vals:
                value = value + "\n" + val

        embed.add_field(name="Locations", value=value)

        value = ""
        async with self.config.pkm() as vals:
            for val in vals:
                value = value + "\n" + val

        embed.add_field(name="Pokemon", value=value)

        value = ""
        async with self.config.exr() as vals:
            for val in vals:
                value = value + "\n" + val

        embed.add_field(name="EX Locations", value=value)

        await ctx.send(content=msg, embed=embed)
