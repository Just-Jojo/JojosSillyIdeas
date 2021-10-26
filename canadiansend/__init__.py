from .sender import CanadianSend

def setup(bot):
    bot.add_cog(CanadianSend(bot))
