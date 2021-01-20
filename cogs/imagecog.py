import asyncio
import discord
from discord.ext import commands

import requests
import random
import re

from urllib.parse import unquote
from bs4 import BeautifulSoup


class ImageCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.image_url_format = "https://images.search.yahoo.com/search/images?p={query}&vm=p"

    @commands.command()
    async def image(self, ctx: commands.Context, *,  argument, is_random=False):
        await ctx.message.delete()  # delete the user message
        r = requests.get(self.image_url_format.format(query=argument)).content
        soup = BeautifulSoup(r, 'html.parser')
        results = soup.find("ul", {"id": "sres"})
        if results is None:
            return await ctx.send(f"Could not find any images for {argument}.")

        image_urls = f"https://images.search.yahoo.com{results.find('a')['href']}"

        res = requests.get(image_urls)
        matches = re.findall(r"imgurl=(?P<imgurl>.*?)\\", res.text)
        matches = [unquote(x) for x in matches]
        if is_random:
            url = random.choice(matches)
        else:
            url = matches[0]
        if not url.startswith("http"):
            url = "http://" + url

        embed = discord.Embed(title=argument,
                              description=f"Requested by: {ctx.author.display_name}",
                              color=discord.colour.Colour.blurple())
        embed.set_image(url=url)
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("❌")

    @commands.command()
    async def rimage(self, ctx: commands.Context, *, argument):
        await self.image(ctx, argument=argument, is_random=True)


def setup(bot):
    bot.add_cog(ImageCog(bot))
