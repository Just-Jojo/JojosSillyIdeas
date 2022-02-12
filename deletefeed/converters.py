from redbot.core import commands


class NoneChannelConverter(commands.TextChannelConverter):
    async def convert(self, ctx: commands.Context, arg: str):
        if arg == "None":
            return None
        return await super().convert(ctx, arg)
