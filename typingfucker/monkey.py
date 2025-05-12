# MONKE

from redbot.core import commands, Config
from redbot.core.bot import Red
import discord
from discord.context_managers import Typing

original = commands.Context.typing
original_trigger = commands.Context.trigger_typing

class MTyping(Typing):
    async def do_typing(self):
        try:
            super().do_typing()
        except discord.HTTPException:
            pass

    def __enter__(self):
        try:
            return super().__enter__()
        except discord.HTTPException:
            pass

    def __exit__(self, exc_type, exc, tb):
        try:
            return super().__exit__(exc_type, exc, tb)
        except Exception:
            pass

    async def __aenter__(self):
        try:
            return await super().__aenter__()
        except discord.HTTPException:
            pass

    async def __aexit__(self, exc_type, exc, tb):
        try:
            return await super().__aexit__(exc_type, exc, tb)
        except Exception:
            pass

def typing(self):
    return MTyping(self)

async def new_typing(self):
    """ aaaa """

    try:
        return await original_trigger(self)
    except Exception as e:
        pass


class TypingFucker(commands.Cog):
    """Monkey patch typing to not error"""

    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, 544974305445019651, True)
        self.config.register_global(enabled=False)
        self._enabled: bool = None

    def cog_unload(self):
        if self._enabled:
            commands.Context.typing = original
            commands.Context.trigger_typing = original_typing

    async def cog_load(self) -> None:
        await self.fuckup()

    async def fuckup(self):
        self._enabled = e = await self.config.enabled()
        if e:
            commands.Context.typing = typing
            commands.Context.trigger_typing = new_typing

    @commands.is_owner()
    @commands.command()
    async def typefuck(self, ctx: commands.Context):
        """Enable monkeypatch"""

        coro = self.config.enabled
        if await coro():
            return await ctx.send("Typing is already fucked")
        await coro.set(True)
        self._enabled = True
        await ctx.tick()
        commands.Context.typing = typing
        commands.Context.trigger_typing = new_typing

    @commands.is_owner()
    @commands.command()
    async def untypefuck(self, ctx: commands.Context):
        """Disable monkeypatch"""

        coro = self.config.enabled
        if not await coro():
            return await ctx.send("Typing is not fucked")
        await coro.set(False)
        self._enabled = False
        await ctx.tick()

        commands.Context.typing = original
        commands.Context.trigger_typing = original_typing
