from redbot.core import commands, Config


class Paywall(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, 544974305445019651, True)
        self.config.register_global(enabled=False)

    async def bot_check(self, ctx: commands.Context):
        if await self.bot.is_owner(ctx.author) or ctx.command.name == "licenseinfo": # Herk
            return True
        if hasattr(self.bot, "_all_owner_ids") and ctx.author.id in self.bot._all_owner_ids:
            # Sudo shit
            return True
        if not await self.config.enabled():
            return True
        await ctx.send("This bot is now paywalled. Please pay $400 to use this bot. Thanks")
        return False

    @commands.command()
    @commands.is_owner()
    async def paywall(self, ctx: commands.Context):
        coro = self.config.enabled
        data = not await coro()
        now_no_longer = "now" if data else "no longer"
        await ctx.send(f"{ctx.me.name} is {now_no_longer} paywalled!!!")
        await coro.set(data)


async def setup(bot):
    await bot.add_cog(Paywall(bot))
