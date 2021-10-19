from redbot.core import commands


class Throwaway(commands.Cog):
    @commands.command()
    async def throwaway(self, ctx):
        x = 3
        y = 4
        await ctx.send(f"{x + y % 2 = }")


def setup(bot):
    bot.add_cog(Throwaway())
