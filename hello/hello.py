from redbot.core import commands


class Hello:
    """Hello World"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="hello")
    async def world(self, ctx):
        await ctx.send("Hello World")
