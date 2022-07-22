from redbot.core import commands, Config
from redbot.core.bot import Red


class LicenseInfoRemover(commands.Cog):
    """Remove the licenseinfo command honestly"""

    @commands.command()
    @commands.is_owner()
    async def licenseinforemove(self, ctx: commands.Context, please: str = None):
        """Remove the license info command"""
        if please is None:
            return await ctx.send("Say please maybe?")
        elif please.lower() == "please?":
            return await ctx.send("Nah mate, you need a license to run Red, innit?")
        await ctx.send("That wasn't a pleaaaaase!")


def setup(bot: Red) -> None:
    bot.add_cog(LicenseInfoRemover())
