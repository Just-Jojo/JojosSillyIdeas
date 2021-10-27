from .pagify_message import PagifyMessage
from redbot.core.bot import Red


__red_end_user_data_statement__ = "This cog is not yes"

def setup(bot: Red):
    bot.add_cog(PagifyMessage(bot))
