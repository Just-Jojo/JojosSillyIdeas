globals().update({"setup": lambda bot: (asyncio := __import__("asyncio"), redbot := __import__("redbot"), bot.add_cog(type("OneLine", (redbot.core.commands.Cog,), {"__init__": (lambda self, bot: (setattr(self, "bot", bot), setattr(self, "config", redbot.core.Config.get_conf(self, 544974305445019651, True)), self.config.register_global(test=1), None)[-1]), "test": (__import__("redbot").core.commands.command(name="test")(asyncio.coroutine(lambda self, ctx: (yield from ctx.send(f"Hello world fr")))))})(bot))), "teardown": lambda x: x.remove_cog("OneLine")})