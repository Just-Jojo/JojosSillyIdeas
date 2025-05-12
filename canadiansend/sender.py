from __future__ import annotations

from functools import wraps

import discord
from discord.abc import Messageable
from redbot.core import commands, Config
from redbot.core.bot import Red

import string

old_func = Messageable.send


@wraps(old_func)
async def send(
    self: Messageable,
    content: str = None,
    **kwargs: dict
) -> discord.Message:
    if content:
        content = str(content).replace("about", "aboot")
        sep, capitalize = ", ", False
        if content.endswith(","):
            sep = " "
        elif content.endswith(string.punctuation):
            sep, capitalize = "\n", True
        eh = "Eh" if capitalize else "eh"
        content += f"{sep}{eh}?"
    else:
        content = "Eh?"
    return await old_func(self, content=content, **kwargs)


class CanadianSend(commands.Cog):
    """Canadianize your bot, eh?"""

    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, 544974305445019651, True)
        self.config.register_global(enabled=False)

    def cog_unload(self) -> None:
        self._monkey_patch(False)

    async def cog_load(self) -> None:
        if await self.config.enabled():
            self._monkey_patch(True)

    async def cog_check(self, ctx: commands.Context) -> bool:
        return await self.bot.is_owner(ctx.author)

    @commands.group(name="canadiansend", aliases=("cs",))
    async def canadian_send(self, ctx: commands.Context) -> None:
        """Manage canadian settings"""
        pass

    @canadian_send.command(name="enable")
    async def canadian_send_enable(self, ctx: commands.Context) -> None:
        """Enable canadian send"""
        self._monkey_patch(True)
        await ctx.send("Canadian send is now enabled")

    @canadian_send.command(name="disable")
    async def canadian_send_disable(self, ctx: commands.Context) -> None:
        """Disable canadian send"""
        self._monkey_patch(False)
        await ctx.send("Canadian send is now disabled")

    def _monkey_patch(self, patch: bool) -> None:
        func = old_func
        if patch:
            func = send

        setattr(Messageable, "send", func)

    async def red_delete_data_for_user(self, *args, **kwargs):
        return

    async def red_get_data_for_user(self, *args, **kwargs):
        return {}
