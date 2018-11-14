import discord
import random
from redbot.core import commands, Config, checks


class Pkmn(getattr(commands, "Cog", object)):
    """
    Pokemon Management
    """

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=2630175158)
        self.settings = Config.get_conf(None, identifier=602700309, cog_name="Info")
