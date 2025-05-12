from redbot.core import commands, Config
from redbot.core.bot import Red

from typing import Optional


@commands.command(name="help", hidden=True)
async def _help(ctx: commands.Context):
    """Get help for things and shit I guess"""
    await ctx.send("For more help call 1-800-45565-ur-mum.\n\nMoney back is an idiot's dream, no refunds.")


class Perhaps(commands.Cog):
    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, 544974305445019651, True)
        self.config.register_global(enabled=False)
        self._command: Optional[commands.Command] = None

    async def cog_load(self):
        self._inject_eject_cmd(await self.config.enabled())

    def _inject_eject_cmd(self, state: bool) -> None:
        if state:
            self._command = self.bot.remove_command("help")
            self.bot.add_command(_help)
        else:
            maybe_com = self.bot.remove_command("help")
            if self._command:
                self.bot.add_command(self._command)
            else:
                self.bot.add_command(maybe_com)

    @commands.command()
    @commands.is_owner()
    async def helptoggle(self, ctx: commands.Context):
        """Toggle help or something idfk"""
        c = self.config.enabled
        d = not await c()
        await c.set(d)
        await ctx.send(f"Help toggled = {d}")
        self._inject_eject_cmd(d)


async def setup(bot: Red):
    await bot.add_cog(Perhaps(bot))
