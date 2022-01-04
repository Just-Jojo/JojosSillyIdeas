from redbot.core import commands
import discord

import logging

log = logging.getLogger("red.sillyideas.damnedhelp")

class DamnedHelp(commands.Cog):
    @commands.Cog.listener()
    async def on_message_without_command(self, message: discord.Message) -> None:
        if not message.guild:
            log.info(f"no guild {message.author = }")
            return
        elif message.author.bot:
            log.info(f"author was bot {message.author = }")
            return
        elif message.guild.id != 133049272517001216:
            log.info(f"not red {message.author = }")
            return
        elif message.content != "!help":
            log.info(f"not !help {message.author = }")
            return
        await ctx.send(
            "There is no help for the damned.",
            reference=message.to_reference(fail_if_not_exists=False),
            mention_author=False
        )


def setup(bot):
    bot.add_cog(DamnedHelp())
