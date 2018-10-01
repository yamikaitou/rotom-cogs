from .info import Info


def setup(bot):
    bot.remove_command("info")
    n = Info(bot)
    bot.add_cog(n)
