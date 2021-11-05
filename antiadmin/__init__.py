import discord

from redbot.core import commands
from redbot.core.bot import Red
import logging

log = logging.getLogger("red.jojossillyideas.antiadmin")


class AntiAdmin(commands.Cog):
    """Stop fucking idiots who give you admin permissions"""

    __authors__ = "Jojo#7791"
    __version__ = "1.0.0"

    def __init__(self, bot: Red):
        self.bot = bot

    async def red_delete_data_for_user(self, *args, **kwargs):
        return

    def format_help_for_context(self, ctx: commands.Context):
        return (
            f"{super().format_help_for_context(ctx)}\n\n"
            f"**Author:** {self.__authors__}\n"
            f"**Version:** {self.__version__}"
        )

    @commands.command()
    async def antiadminversion(self, ctx: commands.Context):
        await ctx.maybe_send_embed(f"AntiAdmin, version {self.__version__}. Written by {self.__authors__}")

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        me: discord.Member = guild.me
        if not me.guild_permissions.administrator:
            return
        message = "Please, don't give me admin permissions. What if my dev was evil and destroyed your server?"
        try:
            await guild.owner.send(message)
        except discord.HTTPException:
            try:
                chan = [c for c in guild.channels if c.permissions_for(me).send_messages][0]
            except IndexError:
                ... # Fuck your guild then
            else:
                await chan.send(message)

    async def bot_check(self, ctx: commands.Context):
        if not ctx.guild:
            return True
        return not ctx.me.guild_permissions.administrator


__red_end_user_data_statement__ = "No"


def setup(bot: Red):
    bot.add_cog(AntiAdmin(bot))
