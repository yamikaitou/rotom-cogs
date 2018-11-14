import discord
import random
from redbot.core import commands, Config, checks
import aiomysql

try:
    from .sqlkey import *
except:
    raise ImportError("Missing sqlkey.py")


class Gyms(getattr(commands, "Cog", object)):
    """
    Gym Management
    """

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=766459223)
        self.settings = Config.get_conf(None, identifier=602700309, cog_name="Info")

    @commands.command()
    async def gym(self, ctx, *, gym: str):
        await ctx.send(await self.findgym(gym))

    async def findgym(self, gym: str):
        conn = await aiomysql.connect(
            host=SQL_HOST,
            port=3306,
            user=SQL_USER,
            password=SQL_PASS,
            db=SQL_DATA,
            loop=self.bot.loop,
        )
        cur = await conn.cursor()
        await cur.execute("""SELECT * FROM gyms WHERE Name = "{}";""".format(gym))

        r = await cur.fetchall()
        await cur.close()
        conn.close()

        return r[0]
