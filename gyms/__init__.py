from .gyms import Gyms


def setup(bot):
    bot.add_cog(Gyms(bot))
