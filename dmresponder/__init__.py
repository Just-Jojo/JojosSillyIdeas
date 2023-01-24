# Copyright (c) 2023 - Jojo#7791
# Licensed under MIT
from __future__ import annotations
from redbot.core import commands, Config
from redbot.core.bot import Red

from .utils import ChannelConverter
import discord


class DMResponder(commands.Cog):
    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, 544974305445019651, True)
        self.config.register_global(dm_channel=None)

    async def cog_check(self, ctx: commands.Context) -> bool:
        return ctx.guild and await ctx.bot.is_owner(ctx.author)

    @commands.group(name="dmresponder", aliases=["dmr"])
    async def dm_responder(self, ctx: commands.Context):
        """Commands relating to the DM Responder"""

    @dm_responder.command(name="channel")
    async def dm_responder_channel(self, ctx: commands.Context, channel: ChannelConverter):
        """Set a channel to relay dms from [botname] to
        Type "None" to reset it
        """
        if not channel:
            await self.config.dm_channel.clear()
            return await ctx.tick()
        if not channel.permissions_for(ctx.me).embed_links:
            return await ctx.send("I cannot send embeds there, please enable this permission and set this channel again.")
        await self.config.dm_channel.set(channel.id)
        await ctx.tick()

    @dm_responder.command(name="respond")
    async def dm_responder_respond(self, ctx: commands.Context, user: discord.User, *, message: str):
        """Send a message to a user in dms"""
        try:
            await user.send(message)
        except discord.Forbidden:
            return await ctx.send("I could not send your message to that user.")
        await ctx.tick()

    @commands.Cog.listener("on_message_without_command")
    async def dm_responder_listener(self, msg: discord.Message):
        if msg.author.bot:
            return
        if msg.guild:
            return
        if not await self.config.dm_channel():
            return
        channel = self.bot.get_channel(await self.config.dm_channel())
        if not channel:
            return
        embed = discord.Embed(
            description=msg.content,
            colour=await self.bot.get_embed_colour(None),
            timestamp=msg.created_at
        ).set_author(name=f"Dm from {msg.author.name} ({msg.author.id})", icon_url=msg.author.avatar.url)
        if msg.stickers:
            sticker: discord.Sticker = msg.stickers[0]
            embed.set_image(url=sticker.url)
        await channel.send(embed=embed)


async def setup(bot: Red):
    await bot.add_cog(DMResponder(bot))
