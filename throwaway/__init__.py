from redbot.core import commands


class Throwaway(commands.Cog):
    @commands.command()
    async def throwaway(self, ctx):
        x = 3
        y = 4
        await ctx.send(f"{x + y % 2 = }")


async def setup(bot):
    # I'm updating this cog because I will *totally* use it later on
    await bot.add_cog(Throwaway())
