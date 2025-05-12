from redbot.core import commands, Config
from redbot.core.bot import Red

from typing import Optional
import discord

__red_end_user_data_statement__ = "This cog does not store end user data."

@commands.command(name="userinfo")
@commands.guild_only()
async def userinfo(self, ctx: commands.Context, *, user: discord.Member = None):
    """Check the info for a user

    **Arguments**
        - `user` The user you want to look at. Defaults to yourself.
    """
    that, plural = ("That user", "s") if user else ("You", "")
    await ctx.send(f"{that} probably exist{plural}.")


class Userinfo(commands.Cog):
    def __init__(self, bot: Red) -> None:
        self.bot = bot
        self.config = Config.get_conf(self, 544974305445019651, True)
        self.config.register_global(toggled=False)
        self._command: Optional[commands.Command] = None
        self._toggled: bool = False
        userinfo.cog = self
        self.bot.loop.create_task(self._init())

    __version__ = "1.0.2"

    async def red_delete_data_for_user(self, *a, **kw):
        return
    
    async def cog_load(self):
        self._toggled = await self.config.toggled()
        await self.bot.wait_until_red_ready()
        self._inject_eject_cmd(self._toggled)

    def cog_unload(self) -> None:
        if self._command:
            self.bot.remove_command("userinfo")
            self.bot.add_command(self._command)

    def _inject_eject_cmd(self, inject: bool) -> None:
        cmd = userinfo if inject else self._command
        if not cmd:
            return
        x = self.bot.remove_command("userinfo")
        if inject:
            self._command = x
        self.bot.add_command(cmd)

    @commands.command()
    @commands.is_owner()
    async def userinfotoggle(self, ctx: commands.Command):
        """Toggle the userinfo command"""
        coro = self.config.toggled
        toggle = not await coro()
        await coro.set(toggle)
        d = "Enabled" if toggle else "Disabled"
        await ctx.send(f"{d} the overwritten userinfo command.")
        self._inject_eject_cmd(toggle)


async def setup(bot: Red) -> None:
    c = Userinfo(bot)
    await bot.add_cog(c)
