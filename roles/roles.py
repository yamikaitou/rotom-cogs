import discord
from redbot.core import commands, checks


class Roles:
    """
    Role Management
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def role(self, ctx, rolename = None):
        """
        Adds a role to the user

        :param rolename: Role Name
        """

        if rolename is None:
            embed = discord.Embed(
                title="Available Roles",
                colour=discord.Colour(0x329077),
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

            await ctx.send(embed=embed)
        else:
            role = discord.utils.get(ctx.guild.roles, name=rolename)
            if role not in ctx.author.roles:
                await ctx.author.add_roles(role)
                await ctx.send("I have given you the role")
            else:
                await ctx.author.remove_roles(role)
                await ctx.send("I have taken the role from you")

