import discord
from discord.ext import commands

import random


class RandomCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.numbers = {"0": "0️⃣", "1": "1️⃣", "2": "2️⃣", "3": "3️⃣", "4": "4️⃣",
                        "5": "5️⃣", "6": "6️⃣", "7": "7️⃣", "8": "8️⃣", "9": "9️⃣"}

    @commands.command(name="d")
    async def roll_dice(self, ctx: commands.Context, number: str):
        if len(number) > 50:
            msg = await ctx.send(f"bruh")
            await msg.add_reaction("❌")
            return
        if not number.isdigit():
            msg = await ctx.send(f"!d <int>")
            await msg.add_reaction("❌")
            return
        number = str(random.randint(0, int(number)))
        response = "".join(self.numbers[x] for x in number)
        msg = await ctx.send(response)
        await msg.add_reaction("❌")

    @commands.command(name="decide")
    async def decide_between(self, ctx: commands.Context, *, arguments):
        arguments = arguments.split(";")
        await ctx.send(f"The bot has decided: {random.choice(arguments)}!")


def setup(bot):
    bot.add_cog(RandomCog(bot))
