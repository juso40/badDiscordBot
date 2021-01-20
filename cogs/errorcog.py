import discord
from discord.ext import commands


class ErrorCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Command !{ctx.command} requires additional arguments.")


def setup(bot):
    bot.add_cog(ErrorCog(bot))
