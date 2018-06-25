import discord
import random
from redbot.core import commands


class Roles:
    """
    Role Management
    """

    def __init__(self, bot):
        self.bot = bot

    def role_assign():
        def predicate(ctx):
            return ctx.message.channel.id == 460650422986735626 or ctx.message.channel.id == 362798066199298049

        return commands.check(predicate)

    @commands.command()
    @commands.guild_only()
    @role_assign()
    async def role(self, ctx, rolename=None):
        """
        Adds a role to the user

        :param rolename: Role Name
        """

        msg = None

        if rolename is not None:
            try:
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
            description="Select one of the roles below to be added/removed from your profile\n\nExample: !role raids-all\n\n",
        )

        embed.add_field(
            name="Locations",
            value="raids-all\nraids-lew\nraids-fm\nraids-hv\nraids-coppell\nraids-oldtownlew",
        )
        embed.add_field(name="Pokemon", value="perfect\nditto\nunown")
        embed.add_field(
            name="EX Locations",
            value="grove-park\nstaton-oak-park\ntealwood-oaks-park\nspring-meadow-park\nforest-vista-fountain\nparkers-square\ngerault-park\njakes-hilltop\nsprint-lew\nstarbucks-fm",
        )

        await ctx.send(content=msg, embed=embed)
