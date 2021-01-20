import discord
from discord.ext import commands


bot = commands.Bot(command_prefix="!")
bot.load_extension("cogs.imagecog")
bot.load_extension("cogs.mathcog")
bot.load_extension("cogs.codecog")
bot.load_extension("cogs.randomcog")
bot.load_extension("cogs.errorcog")


@bot.event
async def on_ready():
    print(f"Beep Boop Beep, Bot-{bot.user} is active!")


@bot.event
async def on_reaction_add(reaction: discord.Reaction, user):
    if user == bot.user:
        return
    if reaction.message.author == bot.user and reaction.emoji == "❌":
        await reaction.message.delete()


commands.client = bot
fp = open("token")
token = fp.readline().strip()
fp.close()
bot.run(token)
