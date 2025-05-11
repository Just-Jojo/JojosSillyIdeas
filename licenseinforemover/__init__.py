from redbot.core import commands, Config
from redbot.core.bot import Red

from typing import Optional


class LicenseInfoRemover(commands.Cog):
    """Remove the licenseinfo command honestly"""

    @commands.command()
    @commands.is_owner()
    async def licenseinforemove(self, ctx: commands.Context, please: Optional[str] = None):
        """Remove the license info command"""
        if please is None:
            await ctx.send("Say please, maybe?")
            return
        elif please.lower() == "please?":
            await ctx.send("Nah man, you need a license to run Red. That's kinda fucked up, dude...")
            return
        await ctx.send("That wasn't a pleaaaaase!")


async def setup(bot: Red) -> None:
    await bot.add_cog(LicenseInfoRemover())
