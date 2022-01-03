from redbot.core import commands
from redbot.core.bot import Red

from typing import Optional
import discord

__red_end_user_data_statement__ = "This cog does not store end user data."


class Userinfo(commands.Cog):
    def __init__(self, bot: Red) -> None:
        self.bot = bot
        self._command: Optional[commands.Command] = None

    @classmethod
    async def init(cls, bot: Red) -> "Userinfo":
        self = cls(bot)
        self._command = bot.remove_command("userinfo")
        return self

    @commands.command(name="userinfo")
    @commands.guild_only()
    async def userinfo(self, ctx: commands.Context, user: discord.Member = None):
        """Check the info for a user

        **Arguments**
            - `user` The user you want to look at. Defaults to yourself.
        """
        that, plural = ("That user", "s") if user else ("You", "")
        await ctx.send(f"{that} probably exist{plural}.")


async def setup(bot: Red) -> None:
    c = await Userinfo.init(bot)
    bot.add_cog(c)
