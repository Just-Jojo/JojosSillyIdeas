# Copyright (c) 2021 - Jojo#7791
# Licensed under MIT

from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.utils.chat_formatting import (
    box,
    humanize_number as hn,
    humanize_list as hl,
)
import random
import discord
from discord.utils import copy_doc

from functools import partial


@copy_doc(hl)
def humanize_list(items, **kwargs):
    items = [f"`{item}`" for item in items]
    return hl(items, **kwargs)


class RandomPatterns(commands.Cog):
    """Generate random patterns"""

    __authors__ = ["Jojo#7791"]
    __version__ = "1.0.0"

    def __init__(self, bot: Red):
        self.bot = bot

    def format_help_for_context(self, ctx):
        plural = "" if len(self.__authors__) == 1 else "s"
        return (
            f"{super().format_help_for_context(ctx)}\n"
            f"**Author{plural}:** {humanize_list(self.__authors__)}\n"
            f"**Version:** {self.__version__}"
        )

    @commands.command()
    async def randpattern(self, ctx: commands.Context, lines: int = 5):
        """Generate a random pattern"""
        if lines < 1:
            return await ctx.maybe_send_embed(
                f"Silly you, you can't generate {hn(lines)} lines!"
            )
        async with ctx.typing():
            func = partial(self._gen_outcome, lines)
            outcome = await self.bot.loop.run_in_executor(None, func)
        try:
            await ctx.maybe_send_embed(box(outcome))
        except ValueError:
            await ctx.maybe_send_embed(box(outcome[:1980]))

    def _gen_outcome(self, lines):
        fields = []
        outcome = ""
        [fields.append([]) for _ in range(lines)]
        chars = ["^", "*", "&", "$", "%", "[", "]", "{", "}", "#", "<", ">"]
        white_space = [" "] * 10
        chars.extend(white_space)
        for field in fields:
            [field.append(random.choice(chars)) for _ in range(50)]
            outcome += "".join(field) + "\n"
        return outcome
