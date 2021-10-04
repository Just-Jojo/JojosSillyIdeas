# MONKE

from redbot.core import commands, Config
from redbot.core.bot import Red
from discord.context_managers import Typing

original = commands.Context.typing
original_trigger = commands.Context.trigger_typing

class MTyping(Typing):
    def __init__(self, messageable):
        ...

    async def do_typing(self):
        ...

    def __enter__(self):
        ...

    def __exit__(self, exc_type, exc, tb):
        ...

    async def __aenter__(self):
        ...

    async def __aexit__(self, exc_type, exc, tb):
        ...

def typing(self):
    return MTyping(self)

async def new_typing(self):
    """ aaaa """

    ...


class TypingFucker(commands.Cog):
    """Monkey patch typing to not error"""

    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, 544974305445019651, True)
        self.config.register_global(enabled=False)
        self.task = self.bot.loop.create_task(self.fuckup())
        self._enabled: bool = None

    def cog_unload(self):
        self.task.cancel()
        if self._enabled:
            commands.Context.typing = original
            commands.Context.trigger_typing = original_typing

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
