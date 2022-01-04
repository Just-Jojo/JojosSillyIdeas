import asyncio

import discord
from redbot.core import commands, Config
from redbot.core.utils.predicates import MessagePredicate
from redbot.vendored.discord.ext import menus
import contextlib

import datetime
from typing import List, Union, Dict
import logging

log = logging.getLogger("red.jojossillyideas.mayor.menus")
emojis = (
    "\N{DIGIT ONE}\N{VARIATION SELECTOR-16}\N{COMBINING ENCLOSING KEYCAP}",
    "\N{DIGIT TWO}\N{VARIATION SELECTOR-16}\N{COMBINING ENCLOSING KEYCAP}",
    "\N{DIGIT THREE}\N{VARIATION SELECTOR-16}\N{COMBINING ENCLOSING KEYCAP}",
    "\N{DIGIT FOUR}\N{VARIATION SELECTOR-16}\N{COMBINING ENCLOSING KEYCAP}",
    "\N{DIGIT FIVE}\N{VARIATION SELECTOR-16}\N{COMBINING ENCLOSING KEYCAP}",
)


def get_timestamp() -> datetime.datetime:
    return datetime.datetime.now(tz=datetime.timezone.utc)


class Page(menus.ListPageSource):
    def __init__(self, pages: List[str], *, title: str):
        super().__init__(pages, per_page=1)
        self.title = title

    async def format_page(self, menu: "Menu", page: str) -> Dict[str, Union[discord.Embed, str]]:
        footer = f"Page {menu.current_page + 1}/{self.get_max_pages()}"
        timestamp = get_timestamp()
        kwargs = {
            "content": (
                f"**{self.title}**\n\n"
                f"{page}\n"
                f"{footer} | <t:{int(timestamp.timestamp())}>"
            ),
        }
        if await menu.ctx.embed_requested():
            embed = discord.Embed(
                title=self.title,
                description=page,
                timestamp=timestamp,
                colour=await menu.ctx.embed_colour(),
            ).set_footer(text=footer)
            kwargs = {"embed": embed}
        return kwargs

    def is_paginating(self) -> bool:
        return True


class Menu(menus.MenuPages, inherit_buttons=False):
    def __init__(self, source: Page):
        super().__init__(source, clear_reactions_after=True)

    @property
    def source(self) -> Page:
        return self._source

    async def show_checked_page(self, page_number: int) -> None:
        max_pages = self.source.get_max_pages()
        try:
            if max_pages > page_number >= 0:
                await self.show_page(page_number)
            elif max_pages <= page_number:
                await self.show_page(0)
            elif 0 > page_number:
                await self.show_page(max_pages - 1)
        except IndexError:
            pass

    def _skip_single_triangle_buttons(self) -> bool:
        return not (max_pages := self.source.get_max_pages()) or max_pages == 1

    def _skip_double_triangle_buttons(self) -> bool:
        return not (max_pages := self.source.get_max_pages()) or max_pages <= 5

    @menus.button(
        "\N{BLACK LEFT-POINTING TRIANGLE}\N{VARIATION SELECTOR-16}",
        position=menus.First(1),
        skip_if=_skip_single_triangle_buttons,
    )
    async def go_to_previous_page(self, payload):
        await self.show_checked_page(self.current_page - 1)

    @menus.button(
        "\N{BLACK RIGHT-POINTING TRIANGLE}\N{VARIATION SELECTOR-16}",
        position=menus.Last(0),
        skip_if=_skip_single_triangle_buttons,
    )
    async def go_to_next_page(self, payload):
        await self.show_checked_page(self.current_page + 1)

    @menus.button("\N{CROSS MARK}")
    async def stop_pages(self, payload):
        self.stop()
        await self.message.delete()

    @menus.button(
        "\N{BLACK RIGHT-POINTING DOUBLE TRIANGLE}\N{VARIATION SELECTOR-16}",
        position=menus.Last(1),
        skip_if=_skip_double_triangle_buttons,
    )
    async def go_to_last_page(self, payload):
        await self.show_page(self.source.get_max_pages() - 1)

    @menus.button(
        "\N{BLACK LEFT-POINTING DOUBLE TRIANGLE}\N{VARIATION SELECTOR-16}",
        position=menus.First(0),
        skip_if=_skip_double_triangle_buttons,
    )
    async def go_to_first_page(self, payload):
        await self.show_page(0)


class VotingSource(menus.ListPageSource):
    def __init__(self, candidates: List[discord.Member]):
        self.candidates: List[List[discord.Member]] = []
        for i in range(0, len(candidates), 5):
            self.candidates.append(candidates[i:i+5])
        super().__init__(self.candidates, per_page=1)

    def is_paginating(self) -> bool:
        return True

    async def format_page(self, menu: "Menu", page: List[discord.Member]) -> Union[str, discord.Embed]:
        ctx: commands.Context = menu.ctx
        data = "\n".join(f"{emojis[i]} {page[i]}" for i in range(5))
        instructions = "Press the emoji of the candidate that you would like to vote for."
        footer = f"Page {menu.current_page + 1}/{self.get_max_pages()}"
        timestamp = get_timestamp()
        if await ctx.embed_requested():
            ret = discord.Embed(
                title="Mayoral Candidates",
                description=data,
                timestamp=timestamp,
                colour=await ctx.embed_colour(),
            ).set_footer(text=f"{instructions} | {footer}")
            return ret
        return (
            "Mayoral Candidates\n\n"
            f"{data}\n"
            f"{instructions}\n"
            f"{footer} | <t:{int(timestamp.timestamp())}>"
        )


class VotingMenu(menus.MenuPages, inherit_buttons=False):
    def __init__(self, source: VotingSource, config: Config):
        self.config = config
        super().__init__(source, clear_reactions_after=True)

    async def _get_vote_confirmation(self, vote: discord.Member) -> None:
        msg = await self.ctx.send(f"Would you like to vote for {str(vote)}? (y/n)")
        pred = MessagePredicate.yes_or_no(ctx=self.ctx, user=self.ctx.author)
        try:
            await self.bot.wait_for("message", check=pred)
        except asyncio.TimeoutError:
            pass
        with contextlib.suppress(discord.HTTPException):
            await msg.delete()
        if not pred.result:
            return
        self.stop()
        async with self.config.votes() as votes:
            try:
                votes[str(vote.id)] += 1
            except KeyError:
                votes[str(vote.id)] = 1
        await self.config.user_from_id(self._author_id).voted.set(True)
        await self.ctx.send("Thank you for voting!")

    @property
    def source(self) -> VotingSource:
        return self._source

    @menus.button(emojis[0], position=menus.First(0))
    async def candidate_one(self, payload):
        try:
            user = self.source.candidates[self.current_page][0]
        except IndexError:
            return
        await self._get_vote_confirmation(user)

    @menus.button(emojis[1], position=menus.First(1))
    async def candidate_two(self, payload):
        try:
            user = self.source.candidates[self.current_page][1]
        except IndexError:
            return
        await self._get_vote_confirmation(user)

    @menus.button(emojis[2], position=menus.First(2))
    async def candidate_three(self, payload):
        try:
            user = self.source.candidates[self.current_page][2]
        except IndexError:
            return
        await self._get_vote_confirmation(user)

    @menus.button(emojis[3], position=menus.First(3))
    async def candidate_four(self, payload):
        try:
            user = self.source.candidates[self.current_page][3]
        except IndexError:
            return
        await self._get_vote_confirmation(user)

    @menus.button(emojis[4], position=menus.First(4))
    async def candidate_five(self, payload):
        try:
            user = self.source.candidates[self.current_page][4]
        except IndexError:
            return
        await self._get_vote_confirmation(user)

    @menus.button("\N{CROSS MARK}", position=menus.Last(0))
    async def stop_pages(self, payload):
        self.stop()
        await self.message.delete()

    def _skip_single_buttons(self):
        if not (max_pages := self.source.get_max_pages()):
            return True
        return max_pages == 0

    @menus.button(
        "\N{BLACK LEFT-POINTING TRIANGLE}\N{VARIATION SELECTOR-16}",
        position=menus.Last(1),
        skip_if=_skip_single_buttons,
    )
    async def go_to_previous_page(self, payload):
        await self.show_checked_page(self.current_page - 1)

    @menus.button(
        "\N{BLACK RIGHT-POINTING TRIANGLE}\N{VARIATION SELECTOR-16}",
        position=menus.Last(2),
        skip_if=_skip_single_buttons,
    )
    async def go_to_next_page(self, payload):
        await self.show_checked_page(self.current_page + 1)

    async def show_checked_page(self, page_number: int) -> None:
        max_pages = self.source.get_max_pages()
        try:
            if max_pages > page_number >= 0:
                await self.show_page(page_number)
            elif max_pages <= page_number:
                await self.show_page(0)
            elif page_number < 0:
                await self.show_page(max_pages - 1)
        except IndexError:
            pass
