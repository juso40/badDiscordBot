import asyncio
import discord
from discord.ext import commands

import praw
import requests
import random
import re

from urllib.parse import unquote
from bs4 import BeautifulSoup

_reddit_file = open("redditsecret")
try:
    _secret, _client_id, _useragent = _reddit_file.readline().split(";")
except:
    _secret, _client_id, _useragent = None, None, None
finally:
    _reddit_file.close()


class ImageCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.image_url_format = "https://images.search.yahoo.com/search/images?p={query}&vm=p"
        self.reddit_url = "https://www.reddit.com/{subreddit}/?include_over_18=on&sort=hot&t=all"
        if _secret and _client_id and _useragent:
            self.reddit = praw.Reddit(client_id=_client_id, client_secret=_secret,
                                      user_agent=_useragent.strip())
            self.reddit.read_only = True
        else:
            self.reddit = None

    @commands.command(description="Find an image for your provided arguments", help="Find an image on the www")
    async def image(self, ctx: commands.Context, *, argument, is_random=False):
        await ctx.message.delete()  # delete the user message
        try:
            r = requests.get(self.image_url_format.format(query=argument)).content
            soup = BeautifulSoup(r, "html.parser")
        except Exception as e:
            await ctx.send(repr(e))
            return
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

    @commands.command(description="Find a random image for your provided arguments",
                      help="Find a random image for your arguments")
    async def rimage(self, ctx: commands.Context, *, argument):
        await self.image(ctx, argument=argument, is_random=True)

    @commands.command(name="reddit", description="Finds a random image from your provided subreddit.")
    async def reddit_finder(self, ctx: commands.Context, subreddit):
        if not self.reddit:
            return await ctx.send("No reddit credentials provided. This command will do nothing.")
        self.reddit: praw.Reddit
        _subreddit = list(self.reddit.subreddit(subreddit).hot(limit=50))
        random.shuffle(_subreddit)
        for x in _subreddit:
            # Get the link of the submission
            url = str(x.url)
            # Check if the link is an image
            if url.endswith("jpg") or url.endswith("jpeg")\
                    or url.endswith("png") or url.endswith("gif") or url.endswith("mp4"):
                embed = discord.Embed(title=f"r/{subreddit}: {x.title}",
                                      description=f"Requested by: {ctx.author.display_name}",
                                      color=discord.colour.Colour.blurple(),
                                      url=f"https://reddit.com{x.permalink}")
                embed.set_image(url=url)
                msg = await ctx.send(embed=embed)
                return await msg.add_reaction("❌")

        await ctx.send(f"Could not find any image in the top 50 hot posts for the given subreddit r/{subreddit}!")


def setup(bot):
    bot.add_cog(ImageCog(bot))
