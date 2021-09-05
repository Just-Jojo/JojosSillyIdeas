# Copyright (c) 2021 - Jojo#7791
# Licensed under MIT

import asyncio

from redbot.core import commands, Config
from redbot.core.utils.chat_formatting import pagify
import discord
from discord.utils import copy_doc


_OG_FUNC = discord.abc.Messageable.send


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
    mention_author=None
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
        "mention_author": mention_author
    }
    if content:
        content = str(content)
        if len(content) > 2000:
            for page in pagify(content):
                async with self.typing():
                    await _OG_FUNC(self, page, **kwargs)
                    await asyncio.sleep(0.5)
            return
    kwargs["content"] = content
    await _OG_FUNC(self, **kwargs)


class PagifyMessage(commands.Cog):
    """Monkey Patch discord.py's send attr to use pagify if message content is over the limit"""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, 544974305445019651, True)
        self.config.register_global(enabled=False)
        self._enabled: bool
        self.init_task = self.bot.loop.create_task(self.init())

    def cog_unload(self):
        self.init_task.cancel()
        if self._enabled:
            setattr(discord.abc.Messageable, "send", _OG_FUNC)

    async def init(self):
        self._enabled = await self.config.enabled()

        if self._enabled:
            setattr(discord.abc.Messageable, "send", new_send)

    async def cog_check(self, ctx: commands.Context):
        return await self.bot.is_owner(ctx.author)

    @commands.group(aliases=["pm"])
    async def pagifymessage(self, ctx: commands.Context):
        """Commands for the pagify message cog"""
        pass

    @pagifymessage.command()
    async def enable(self, ctx: commands.Context):
        await ctx.tick()
        self._enabled = True
        setattr(discord.abc.Messageable, "send", new_send)

    @pagifymessage.command()
    async def disable(self, ctx: commands.Context):
        await ctx.tick()
        self._enabled = False
        setattr(discord.abc.Messageable, "send", _OG_FUNC)
