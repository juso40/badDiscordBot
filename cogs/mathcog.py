import asyncio
import discord
from discord.ext import commands

import numexpr3


class MathCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Simple math evaluation", help="Evaluates your math string")
    async def math(self, ctx, *, argument):
        argument = argument.replace("`", "").replace("\\", "")
        try:
            await ctx.send(numexpr3.evaluate(argument))
        except Exception as e:
            await ctx.send(f"{repr(e)}")


def setup(bot):
    bot.add_cog(MathCog(bot))
