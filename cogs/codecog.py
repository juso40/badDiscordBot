import asyncio
import discord
from discord.ext import commands

import requests
import json
import re

from urllib.parse import urlencode


class CodeCog(commands.Cog):
    def __int__(self, bot):
        self.bot = bot
        self.code_url = "https://ide.geeksforgeeks.org/main.php"

    @commands.command()
    async def code(self, ctx, *, argument):
        cleaned_up = argument.replace("```", "")
        language = cleaned_up.split("\n", maxsplit=1)[0].strip()
        if not language:
            await ctx.send("Missing language argument!")
        code = cleaned_up.replace(language, "")
        print(code)
        data = {
            'lang': language,
            'code': code,
            'input': None,
            'save': False
        }
        header = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'}
        response = requests.get(self.code_url, headers=header, data=data)

        print(response)
        if response["error"]:
            ctx.send(response["error"])
        await asyncio.sleep(0.5)
        _id = response["id"]
        response = requests.get(self.code_details_url.format(id=_id))
        print(response.json())

        print(repr(argument))


def setup(bot):
    bot.add_cog(CodeCog(bot))
