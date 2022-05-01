# Copyright (c) 2022 - Jojo#7791
# Licensed under MIT

from __future__ import annotations

import aiohttp
import discord

from redbot.core import commands, Config
from redbot.core.bot import Red
from redbot.core.utils.chat_formatting import pagify, box

import uma

from typing import Optional
import datetime

import logging

log = logging.getLogger("red.jojocogs.mcoc")


class MCOC(commands.Cog):
    def __init__(self, bot: Red):
        super().__init__()
        self.bot = bot
        self.client = uma.UMAClient(self.bot.loop)

    def cog_unload(self) -> None:
        self.bot.loop.create_task(self.client.close())

    @commands.group()
    async def mcoc(self, ctx: commands.Context):
        pass

    @mcoc.command(name="champ")
    async def mcoc_champ(self, ctx: commands.Context, tier: Optional[int], rank: Optional[int], *, champion: str):
        """Get champion info fr"""

        champion = champion.lower()
        try:
            data = await self.client.get_champ(champion, tier or 6, rank or 3)
        except uma.ChampionException as e:
            if e.args:
                return await ctx.send(e.args[0])
            return await ctx.send_help()
        except uma.APIException:
            return await ctx.send("I'm sorry, the api is down")
        month, day, year = data.released.split("/")
        released = datetime.datetime(int(year), int(month), int(day), tzinfo=datetime.timezone.utc)
        description = (
            "**General Stats**\n\n"
            f"Attack: {data.attack}\n"
            f"Block Prof: {data.block_prof}\n"
            f"Challenger Rating: {data.challenger_rating}\n"
            f"Crit Rate: {data.crit_rate}\n"
            f"Crit Damage: {data.crit_dmge}\n"
            f"Crit Resist: {data.crit_resist}\n"
            f"Energy Resist: {data.energy_resist}\n"
            f"HP: {data.hp}\n"
            f"Physical Resist: {data.physical_resist}\n"
            f"Prestige: {data.prestige}"
        )
        name = " ".join(x.capitalize() for x in data.name.split(" "))
        embed = discord.Embed(
            title=f"{name} {data.tier}\N{WHITE MEDIUM STAR}\N{VARIATION SELECTOR-16} R{data.rank}",
            colour=await ctx.embed_colour(),
            description=description,
            timestamp=datetime.datetime.now(datetime.timezone.utc),
        ).set_author(name=name, url=data.url_page).add_field(
            name="Sig Info", value=si if isinstance((si := data.sig_info), str) else si[-1],
        ).add_field(
            name="Tags", value=", ".join(data.tags)
        ).add_field(
            name="Released", value=f"<t:{int(released.timestamp())}:d>"
        ).set_footer(text="Built with the UMA api (thanks!)")

        await ctx.send(embed=embed)

    @mcoc.command(name="node")
    async def mcoc_node(self, ctx: commands.Context, node: int):
        """Get info about a node from mcoc"""

        # TODO Find a way to query the api for a node name
        try:
            data = await self.client.get_node(node)
        except uma.NodeException as e:
            if e.args:
                return await ctx.send(e.args[0])
            return await ctx.send_help()
        except uma.APIException:
            return await ctx.send("I'm sorry, the api is down")
        embed = discord.Embed(
            title=data.node_name,
            description=data.node_info,
            colour=await ctx.embed_colour(),
        ).set_footer(text="Built with the UMA api (thanks!)")

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(MCOC(bot))
