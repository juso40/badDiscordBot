import discord
from discord.ext import commands

import random
import requests
from bs4 import BeautifulSoup


class GamesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Finds a random game on itch.io with your provided tags", help="Find a random game")
    async def game(self, ctx: commands.Context, *, tags=None):
        url = "https://itch.io/games/new-and-popular/free/platform-web/"
        if tags:
            tags = tags.split()
            for tag in tags:
                url += f"tag-{tag}/"

        try:
            res = requests.get(url).text
            soup = BeautifulSoup(res, "html.parser")
        except Exception as e:
            await ctx.send(repr(e))
            return

        games = soup.find_all("a", {"class": "thumb_link game_link"})
        if not games:
            await ctx.send(f"Could not find any games for following tags: {tags}")
            return
        await ctx.send(random.choice(games)["href"])


def setup(bot):
    bot.add_cog(GamesCog(bot))
