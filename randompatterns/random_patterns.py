# Copyright (c) 2021 - Jojo#7791
# Licensed under MIT

from redbot.core import commands
from redbot.core.utils.chat_formatting import box, humanize_number as hn
import random
import discord

from functools import partial


class RandomPatterns(commands.Cog):
    """Generate random patterns"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def randpattern(self, ctx: commands.Context, lines: int = 5):
        """Generate a random pattern"""
        if lines < 1:
            return await ctx.maybe_send_embed(f"Silly you, you can't generate {hn(lines)} lines!")
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
