import discord

from redbot.core import commands, Config
from redbot.core.bot import Red
from redbot.core.utils.chat_formatting import pagify
import logging

log = logging.getLogger("red.jojossillyideas.antiadmin")


class AntiAdmin(commands.Cog):
    """Stop fucking idiots who give you admin permissions"""

    __authors__ = "Jojo#7791"
    __version__ = "1.0.3"

    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, 544974305445019651, True)
        self.config.register_global(ignore_messages=True, whitelist=[])

    async def red_delete_data_for_user(self, *args, **kwargs):
        return

    def format_help_for_context(self, ctx: commands.Context):
        return (
            f"{super().format_help_for_context(ctx)}\n\n"
            f"**Author:** {self.__authors__}\n"
            f"**Version:** {self.__version__}"
        )

    @commands.command()
    async def antiadminversion(self, ctx: commands.Context):
        await ctx.maybe_send_embed(f"AntiAdmin, version {self.__version__}. Written by {self.__authors__}")

    @commands.group()
    @commands.is_owner()
    async def antiadminset(self, ctx: commands.Context):
        """Manage the settings for the anti admin cog"""

    @commands.is_owner()
    @commands.group(name="antiadminwhitelist", aliases=["aawl"])
    async def anti_admin_whitelist(self, ctx: commands.Context):
        """Manage the whitelist for antiadmin"""

    @anti_admin_whitelist.command(name="add")
    async def whitelist_add(self, ctx: commands.Context, guild: discord.Guild):
        """Add a guild to the whitelist"""
        gid = str(guild.id)
        async with self.config.whitelist() as whitelist:
            if gid in whitelist:
                return await ctx.send("That server is already whitelisted")
            whitelist.append(gid)
        await ctx.tick()

    @anti_admin_whitelist.command(name="remove")
    async def whitelist_remove(self, ctx: commands.Context, guild_id: discord.Object):
        gid = str(guild_id.id)
        async with self.config.whitelist() as whitelist:
            if gid not in whitelist:
                return await ctx.send("That server is not whitelisted")
            whitelist.remove(gid)
        await ctx.tick()

    @anti_admin_whitelist.command(name="list")
    async def whitelist_list(self, ctx: commands.Context):
        """View the whitelisted guilds for anti admin"""

    @antiadminset.command(name="ignore")
    async def anti_admin_ignore(self, ctx: commands.Context, toggle: bool):
        """Set whether the cog should ignore a server if it has administrator permissions"""
        now_no_longer = "now" if toggle else "no longer"
        await ctx.send(f"Guilds that I have adminstrator permissions in will {now_no_longer} be ignored.")

    @commands.is_owner()
    @commands.command(name="antiadminview", aliases=["aav"])
    async def anti_admin_view(self, ctx: commands.Context):
        """Show the guilds that I have administrator permissions in"""
        guilds = [g.name for g in self.bot.guilds if g.me.guild_permissions.administrator]
        if not guilds:
            return await ctx.send("There are no guilds that I have administration permissions in")
        msg = f"Here are the guilds that I have administration permission in:\n{', '.join(guilds)}"
        await ctx.send_interactive(pagify(msg))

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        if not guild.me.guild_permissions.administrator:
            return
        await self._handle_guild(guild)

    async def _handle_guild(self, guild: discord.Guild):
        # This message is sponsored by [REDACTED]
        if str(guild.id) in await self.config.whitelist():
            return
        message = "Please, don't give me admin permissions. What if my dev was evil and destroyed your server?"
        try:
            await guild.owner.send(message)
        except discord.HTTPException:
            try:
                chan = [c for c in guild.channels if c.permissions_for(guild.me).send_messages][0]
            except IndexError:
                ... # Fuck your guild then
            else:
                message = f"{guild.owner.mention}, p{message[1:]}"
                await chan.send(message)

    @commands.Cog.listener()
    async def on_guild_role_update(self, before: discord.Role, after: discord.Role):
        if after.guild.me not in after.members:
            return
        if not after.permissions.administrator:
            return
        await self._handle_guild(after.guild)

    async def bot_check(self, ctx: commands.Context):
        if not ctx.guild:
            return True
        if await self.bot.is_owner(ctx.author):
            return True
        if not await self.config.ignore_messages():
            return True
        if str(ctx.guild.id) in await self.config.whitelist():
            return True
        return not ctx.me.guild_permissions.administrator


__red_end_user_data_statement__ = "No"


async def setup(bot: Red):
    await bot.add_cog(AntiAdmin(bot))
