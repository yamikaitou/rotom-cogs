from redbot.core.bot import Red
from .hello import Hello


def setup(bot: Red):
    bot.add_cog(Hello(bot))
