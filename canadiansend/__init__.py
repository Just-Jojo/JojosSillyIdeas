from .sender import CanadianSend
from redbot.core.bot import Red

__red_end_user_data_statement__ = "This cog is not yes"

async def setup(bot: Red):
    await bot.add_cog(CanadianSend(bot))
