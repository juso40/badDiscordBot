import asyncio
import discord
from discord.ext import commands

import requests
import json
import re
import os

from urllib.parse import urlencode

fp = open(os.path.join("hackerearth"))
api_key = fp.readline().strip()
fp.close()


class CodeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.code_url = "https://api.hackerearth.com/v3/code/run/"
        self.language_dict = {"py": "PYTHON3", "c": "C", "cpp": "CPP14", "c++": "CPP14",
                              "java": "JAVA", "cs": "CSHARP", "rust": "RUST"}

    @commands.command()
    async def code(self, ctx, *, argument):
        cleaned_up = argument.replace("```", "")
        language = cleaned_up.split("\n", maxsplit=1)[0].strip().lower()
        if not language:
            await ctx.send("Missing language argument!")
        code = cleaned_up.replace(language, "")

        try:
            data = {
                "client_secret": api_key,
                "source": code.lstrip(),
                "lang": self.language_dict[language],
                "time_limit": 3,
            }
        except Exception as e:
            await ctx.send(repr(e))
            return

        try:
            response = requests.post(self.code_url, data=data)
        except Exception as e:
            await ctx.send(repr(e))
            return

        response = response.json()["run_status"]
        if response["stderr"]:
            await ctx.send(f"```{language}\n{response['stderr']}\n```")
            return

        output = response["output"]
        await ctx.send(f"```{language}\n{output}\n```")


def setup(bot):
    bot.add_cog(CodeCog(bot))
