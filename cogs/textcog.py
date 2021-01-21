import aiohttp
import asyncio
import discord
from discord.ext import commands

import re
from bs4 import BeautifulSoup
import deep_translator


class TextCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.url_emojipedia = "https://emojipedia.org/search/?q={query}"

    @commands.command(description="🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀", help="🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀🦀")
    async def crabravethis(self, ctx: commands.Context, *, argument):
        await ctx.message.delete()

        crabtext = " 🦀 ".join(argument.split())
        crabtext = f"🦀🦀🦀 {crabtext} 🦀🦀🦀"
        await ctx.send(crabtext)

    @commands.command(description="Replaces all u's and o's with UwU's and OwO's", help="UwU/OwO-ifies your text.")
    async def uwu(self, ctx: commands.Context, *, argument):
        await ctx.message.delete()

        def owo(matchobj: re.Match):
            if matchobj.group("uo").lower() == "u":
                return "UwU"
            else:
                return "OwO"

        uwued = re.sub(r"(?P<uo>[uo])", owo, argument, flags=re.IGNORECASE)
        await ctx.send(uwued)

    @commands.command(description="Adds an emoji after each of your words.", help="Adds emojis to your provided text")
    async def emojify(self, ctx: commands.Context, *, argument):
        await ctx.message.delete()

        original_text_dict = {}
        try:
            trans = deep_translator.GoogleTranslator(source="auto", target="en")
            for word in argument.split():
                original_text_dict[word] = trans.translate(word)
        except Exception as e:
            return await ctx.send(repr(e))

        await asyncio.sleep(0.1)
        emoji_dict = {}
        try:
            # gather all emojis async style
            async with aiohttp.ClientSession() as session:
                for word in argument.split():
                    async with session.get(self.url_emojipedia.format(query=original_text_dict[word])) as result:
                        soup = BeautifulSoup(await result.text(), "html.parser").find("ol", {"class": "search-results"})
                        emoji_dict[word] = soup.find("span", {"class": "emoji"}).text
        except Exception as e:
            return await ctx.send(repr(e))

        emojified = ""
        for word in argument.split():
            emojified += f"{word}{emoji_dict[word]} "

        await ctx.send(emojified)


def setup(bot):
    bot.add_cog(TextCog(bot))
