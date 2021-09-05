from .pagify_message import PagifyMessage

def setup(bot):
    bot.add_cog(PagifyMessage(bot))
