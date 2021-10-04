from .monkey import TypingFucker
from redbot.core.bot import Red

__red_end_user_data_statement__ = "No."

def setup(bot):
    bot.add_cog(TypingFucker(bot))