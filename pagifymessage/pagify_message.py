# Copyright (c) 2021 - Jojo#7791
# Licensed under MIT

import asyncio

from redbot.core import commands, Config
from redbot.core.bot import Red
from redbot.core.utils.chat_formatting import pagify, humanize_list as hl, box
import discord
from functools import wraps as copy_doc


_OG_FUNC = getattr(discord.abc.Messageable, "send")


@copy_doc(hl)
def humanize_list(items, **kwargs):
    items = [f"`{item}`" for item in items]
    return hl(items, **kwargs)


@copy_doc(_OG_FUNC)
async def new_send(
    self: discord.abc.Messageable,
    content=None,
    *,
    tts=False,
    embed=None,
    file=None,
    files=None,
    delete_after=None,
    nonce=None,
    allowed_mentions=None,
    reference=None,
    mention_author=None,
):
    kwargs = {
        "tts": tts,
        "embed": embed,
        "file": file,
        "files": files,
        "delete_after": delete_after,
        "nonce": nonce,
        "allowed_mentions": allowed_mentions,
        "reference": reference,
        "mention_author": mention_author,
    }
    if content:
        content = str(content)
        if len(content) > 2000:
            for page in pagify(content):
                async with self.typing():
                    msg = await _OG_FUNC(self, page, **kwargs)
                    await asyncio.sleep(0.5)
            return msg
    kwargs["content"] = content
    return await _OG_FUNC(self, **kwargs)


class PagifyMessage(commands.Cog):
    """Monkey Patch discord.py's send attr to use pagify if message content is over the limit"""

    __authors__ = ["Jojo#7791"]
    __version__ = "1.0.0"

    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, 544974305445019651, True)
        self.config.register_global(enabled=False)
        self._enabled: bool = False
        self.init_task: asyncio.Task = self.bot.loop.create_task(self.init())

    def format_help_for_context(self, ctx: commands.Context):
        plural = "" if len(self.__authors__) == 1 else "s"
        return (
            f"{super().format_help_for_context(ctx)}\n"
            f"**Author{plural}:** {humanize_list(self.__authors__)}\n"
            f"**Version:** `{self.__version__}`"
        )

    def cog_unload(self) -> None:
        if self._enabled:
            setattr(discord.abc.Messageable, "send", _OG_FUNC)

    async def cog_load(self) -> None:
        self._enabled = await self.config.enabled()

        if self._enabled:
            setattr(discord.abc.Messageable, "send", new_send)

    async def cog_check(self, ctx: commands.Context) -> bool:
        return await self.bot.is_owner(ctx.author)

    @commands.group(aliases=["pm"])
    async def pagifymessage(self, ctx: commands.Context):
        """Commands for the pagify message cog"""
        pass

    @pagifymessage.command()
    async def enable(self, ctx: commands.Context):
        """Enable pagifying messages"""

        await ctx.tick()
        self._enabled = True
        setattr(discord.abc.Messageable, "send", new_send)
        await self.config.enabled.set(True)

    @pagifymessage.command()
    async def disable(self, ctx: commands.Context):
        """Disable pagifying messages"""

        await ctx.tick()
        self._enabled = False
        setattr(discord.abc.Messageable, "send", _OG_FUNC)
        await self.config.enabled.set(False)

    async def red_delete_data_for_user(self, *args, **kwargs):
        return

    async def red_get_data_for_user(self, *args, **kwargs):
        return {}
