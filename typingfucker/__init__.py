from .monkey import TypingFucker
from redbot.core.bot import Red

__red_end_user_data_statement__ = "No."

async def setup(bot):
    await bot.add_cog(TypingFucker(bot))