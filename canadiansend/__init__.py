from .sender import CanadianSend
from redbot.core.bot import Red


def setup(bot: Red):
    bot.add_cog(CanadianSend(bot))
