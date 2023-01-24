# Copyright (c) 2023 - Jojo#7791
# Licensed under MIT

from __future__ import annotations

import discord
from redbot.core import commands
from typing import TYPE_CHECKING, Union


if TYPE_CHECKING:
    ChannelConverter = Union[discord.Thread, discord.GuildChannel]
else:

    class ChannelConverter(commands.Converter):
        async def convert(
            self,
            ctx: commands.Context,
            arg: str
        ) -> Union[discord.Thread, discord.GuildChannel]:
            arg = arg.lower()
            if arg == "none":
                return None
            try:
                return await commands.ThreadConverter().convert(ctx, arg)
            except commands.BadArgument:
                return await commands.GuildChannelConverter().convert(ctx, arg)
