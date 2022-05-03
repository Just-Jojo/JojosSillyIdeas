from redbot.core import commands, Config
from redbot.core.bot import Red
import datetime

import discord
import logging

from .converters import NoneChannelConverter


log = logging.getLogger("red.jojossillyideas.deletefeed")


class DeleteFeed(commands.Cog):
    """Delete feeds for admins or something"""

    __author__ = "Jojo#7791"
    __version__ = "1.0.0"

    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, 544974305445019651, True)
        self.config.register_guild(enabled=False, channel=None)

    async def red_delete_data_for_user(self, *args, **kwargs):
        return

    def format_help_for_context(self, ctx):
        return (
            f"{super().format_help_for_context(ctx)}\n"
            f"**Author:** {self.__author__}\n**Version:** {self.__version__}"
        )

    @commands.group()
    @commands.guild_only()
    @commands.admin()
    async def deletefeed(self, ctx: commands.Context):
        """Manage the delete feed for your guild"""

    @deletefeed.command(name="channel")
    async def delete_feed_channel(self, ctx: commands.Context, channel: NoneChannelConverter):
        """Set the channel for the delete feed. Type `None` to reset it."""
        if not channel:
            await self.config.guild(ctx.guild).channel.reset()
            return await ctx.send("Done. I have reset the delete feed channel.")
        if not channel.permissions_for(ctx.me).send_messages:
            return await ctx.send("I cannot type in that channel.")
        await self.config.guild(ctx.guild).channel.set(str(channel.id))
        await ctx.send(f"Done. I have set the delete feed channel to {channel.mention}")

    @deletefeed.command(name="toggle", aliases=["enable", "disable"])
    async def delete_feed_enable(self, ctx: commands.Context):
        """Toggle the delete feed"""
        coro = self.config.guild(ctx.guild).enabled
        data = not await coro()
        await coro.set(data)
        await ctx.send(f"The delete feed is now {'enabled' if data else 'disabled'}")

    @commands.Cog.listener()
    async def on_raw_message_delete(self, msg: discord.RawMessageDeleteEvent):
        if not msg.guild_id:
            return
        if not await self.config.guild_from_id(msg.guild_id).enabled():
            return
        cached_message = msg.cached_message
        if not cached_message:
            return # Can't do much here unfortunately
        if cached_message.author.bot:
            return
        guild = self.bot.get_guild(msg.guild_id)
        channel = guild.get_channel(int(await self.config.guild(guild).channel()))
        if not channel:
            return
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        kwargs = {
            "content": (
                f"**Message deleted by {cached_message.author} ({cached_message.author.id}).**\n"
                f"Message deleted <t:{int(now.timestamp())}> in channel "
                f"{cached_message.channel.mention} ({cached_message.channel.id})\n"
                f"\n**Message content:** `{cached_message.content}`"
            )
        }
        if await self.bot.embed_requested(channel, ...):
            embed = discord.Embed(
                title=f"Message deleted by {cached_message.author} ({cached_message.author.id}).",
                description=(
                    f"Channel: {cached_message.channel.mention} ({cached_message.channel.id})\n"
                    f"Content: `{cached_message.content}`."
                ),
                colour=await self.bot.get_embed_colour(channel),
                timestamp=now,
            )
            embed.set_author(
                name=f"{cached_message.author} ({cached_message.author.id})",
                icon_url=getattr(cached_message.author.avatar, "url", cached_message.author.default_avatar)
            )
            kwargs = {"embed": embed}
        try:
            await channel.send(**kwargs)
        except discord.Forbidden as e:
            log.debug("Could not log deleted message", exc_info=e)


async def setup(bot: Red):
    await bot.add_cog(DeleteFeed(bot))
