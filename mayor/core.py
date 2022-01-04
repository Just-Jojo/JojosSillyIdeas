from redbot.core import commands, Config
from redbot.core.bot import Red
from redbot.core.commands._dpy_reimplements import CheckDecorator
from redbot.core.utils.chat_formatting import pagify

import discord

from typing import List

from .menus import VotingMenu, VotingSource, get_timestamp, Menu, Page
import logging
from random import choice


log = logging.getLogger("red.jojossillyideas.mayor")
_config_structure = {
    "global": {
        "current_mayor": None, # int the id of the current mayor
        "previous_mayors": [], # List[int] the ids of the previous mayors
        "votes": {}, # Dict[int, int] the id of the candidate and their votes
        "open": False, # bool if users should be able to vote
    },
    "user": {
        "voted": False,
    },
}


def mayor() -> CheckDecorator:
    async def pred(ctx: commands.Context) -> bool:
        return ctx.author.id == await ctx.cog.config.current_mayor()
    return commands.check(pred)


class Mayor(commands.Cog):
    """Stuff for a certain server that won't work anywhere else :Kappa:"""

    __version__ = "1.0.0"

    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, 544974305445019651, True)
        [getattr(self.config, f"register_{x}", lambda **yi: yi)(**y) for x, y in _config_structure.items()]

    async def cog_check(self, ctx: commands.Context) -> bool:
        return ctx.guild is not None and ctx.guild.id == 909509066710208523

    @commands.command()
    async def vote(self, ctx: commands.Context, user: discord.Member = None):
        """Do your duty as a citizen of SMS and vote for your favourite candidate"""
        if not await self.config.open():
            return await ctx.send("I'm sorry, you cannot vote at this time.")
        elif await self.config.user(ctx.author).voted():
            return await ctx.send("You already voted!")
        if not user and user.id != await self.config.current_mayor():
            async with self.config.votes() as votes:
                try:
                    votes[str(user.id)] += 1
                except IndexError:
                    votes[str(user.id)] = 1
            await self.config.user(ctx.author).voted.set(True)
            return await ctx.send("Thank you for voting!")
        members = await self._get_candidates(ctx.guild)
        await VotingMenu(VotingSource(members), self.config).start(ctx)

    @commands.command(aliases=["lockvote"])
    @commands.admin()
    async def unlockvote(self, ctx: commands.Context):
        """Toggle whether voting is enabled or not"""
        current = not await self.config.open()
        enabled = "Enabled" if current else "Disabled"
        await self.config.open.set(current)
        await ctx.send(f"{enabled} voting.")

    @commands.command()
    async def mayors(self, ctx: commands.Context):
        """Get the current and previous mayors of SMS"""
        previous = await self.config.previous_mayors()
        c = await self.config.current_mayor()
        current_mayor = ctx.guild.get_member(c)
        data = f"**Current Mayor:** {current_mayor}"
        if previous:
            data += "\n**Previous Mayors:**\n" + "\n".join(previous)
        await Menu(Page(list(pagify(data, page_length=300)), title="Mayors of SMS")).start(ctx)

    @commands.command()
    @commands.admin()
    async def endvoting(self, ctx: commands.Context):
        """End voting for this month"""
        data = await self.config.votes()
        if not data:
            return await ctx.send("I'm sorry, no one has voted yet!")

        old_mayor = ctx.guild.get_member(await self.config.current_mayor())
        async with self.config.previous_mayors() as pm:
            pm.append(str(old_mayor))

        leaderboard = sorted(data.items(), key=lambda x: x[1], reverse=True)
        data = "\n".join(
            f"{num}. **{ctx.guild.get_member(int(key))}:** {value}"
            for num, (key, value) in enumerate(leaderboard[:2], 1)
        )
        mayor = leaderboard[0]
        timestamp = get_timestamp()
        kwargs = {
            "content": (
                f"Mayor votes leaderboard"
                f"{data}"
                f"<t:{int(timestamp.timestamp())}>"
            ),
        }

        if await ctx.embed_requested():
            data = discord.Embed(
                title="Mayor votes leaderboard",
                description=data,
                colour=await ctx.embed_colour()
            )
            kwargs = {"embed": data}

        new_mayor = ctx.guild.get_member(int(mayor[0]))
        await self.config.current_mayor.set(mayor[0])

        await ctx.send(**kwargs)
        await ctx.send(f"Congratulations {new_mayor.mention}! You are now the mayor")

        role = ctx.guild.get_role(925548551847678023)
        try:
            await old_mayor.remove_roles(role, reason="No longer mayor")
        except discord.HTTPException:
            pass
        try:
            await new_mayor.add_roles(role, reason="Elected as mayor")
        except discord.HTTPException:
            await ctx.send("I was unable to add your role, please contact Jojo for your mayor role.")

        for user in await self.config.all_users():
            await self.config.user_from_id(user).voted.clear()

    @commands.command()
    @commands.is_owner()
    async def set_mayor(self, ctx: commands.Context, user: discord.Member):
        await self.config.current_mayor.set(user.id)
        await ctx.tick()

    @commands.command()
    @mayor()
    async def imthemayor(self, ctx: commands.Context):
        """I'm the mayor after all"""
        quotes = {
            "I'd love to talk, but I have matters to attend to. I'm the Mayor after all.",
            "Excuse me, but I'm very busy right now. I'm the Mayor after all.",
            "Far too busy to talk right now. I'm the mayor, after all."
        }
        await ctx.send(choice(quotes))

    async def _get_candidates(self, guild: discord.Guild) -> List[int]:
        p = await self.config.current_mayor()
        return [m for m in guild.members if not m.bot and m.id != p]
