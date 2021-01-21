import discord
from discord.ext import commands


class ErrorCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(f"Command !{ctx.command} requires additional arguments.")
        await ctx.send(f"Oops something went wrong:\n{error.with_traceback(error.__traceback__)}")


def setup(bot):
    bot.add_cog(ErrorCog(bot))
