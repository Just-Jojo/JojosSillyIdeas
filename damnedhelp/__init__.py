from redbot.core import commands
import discord

import asyncio


class DamnedHelp(commands.Cog):
    @commands.Cog.listener()
    async def on_message_without_command(self, message: discord.Message) -> None:
        if not message.guild:
            return
        elif message.author.bot:
            return
        elif message.guild.id != 133049272517001216:
            return
        elif message.content != "!help":
            return
        await asyncio.sleep(5)
        await message.channel.send(
            "There is no help for the damned.",
            reference=message.to_reference(fail_if_not_exists=False),
            mention_author=False
        )


async def setup(bot):
    await bot.add_cog(DamnedHelp())
