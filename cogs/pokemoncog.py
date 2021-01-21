import asyncio
import discord
from discord.ext import commands

import io
import pyautogui
import pydirectinput
from win32gui import GetWindowText, GetForegroundWindow, GetWindowRect


class PokemonCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.desired_window_name = "VisualBoyAdvance"
        self.input_buffer = []
        self.max_input_buffer = 20

        self.last_frame = None

        self.buttons = {"a": "a",
                        "b": "b",
                        "start": "enter",
                        "select": "backspace",
                        "u": "up",
                        "d": "down",
                        "l": "left",
                        "r": "right",
                        }

    @commands.command("pokemon", help="Play Pokemon!")
    async def pokemon_step(self, ctx: commands.Context, button):
        if button not in self.buttons:
            return await ctx.send(f"Only support following keys: {list(self.buttons.keys())}.")
        if len(self.input_buffer) > self.max_input_buffer:
            await ctx.send(f"Input Buffer is full, please wait for the game to process the inputs first.")
        else:
            self.input_buffer.append(button)
            await ctx.send(f"Added your input to the Input Buffer [{len(self.input_buffer) - 1}]")
        if self.desired_window_name not in GetWindowText(GetForegroundWindow()):
            return await ctx.send(f"The Game is either not running or out of focus!")

        while self.input_buffer:
            button = self.input_buffer.pop()
            key = self.buttons[button]
            pydirectinput.press(key)
        rect = GetWindowRect(GetForegroundWindow())
        x = rect[0]
        y = rect[1]
        w = rect[2] - x
        h = rect[3] - y
        image = pyautogui.screenshot(region=(x, y, w, h))
        self.last_frame = image
        arr = io.BytesIO()
        image.save(arr, format='PNG')
        arr.seek(0)
        file = discord.File(arr, filename="pokemon.png")
        await ctx.send(file=file)

    @commands.command("pokemonstatus", description="Get the latest Frame of the current Pokemon Session",
                      help="Get the current Pokemon status")
    async def get_current_pokemon_status(self, ctx: commands.Context):
        if self.last_frame:
            arr = io.BytesIO()
            self.last_frame.save(arr, format='PNG')
            arr.seek(0)
            file = discord.File(arr, filename="pokemon.png")
            await ctx.send(file=file)
            await ctx.send(f"Currently buffered inputs: {[self.buttons[x] for x in self.input_buffer]}")
            return

        if self.desired_window_name not in GetWindowText(GetForegroundWindow()):
            return await ctx.send(f"The Game is either not running or out of focus! And no last frame exists.\n"
                                  f"Currently buffered inputs: {[self.buttons[x] for x in self.input_buffer]}")

        rect = GetWindowRect(GetForegroundWindow())
        x = rect[0]
        y = rect[1]
        w = rect[2] - x
        h = rect[3] - y
        image = pyautogui.screenshot(region=(x, y, w, h))
        self.last_frame = image
        arr = io.BytesIO()
        image.save(arr, format='PNG')
        arr.seek(0)
        file = discord.File(arr, filename="pokemon.png")
        await ctx.send(file=file)
        await ctx.send(f"Currently buffered inputs: {[self.buttons[x] for x in self.input_buffer]}")

def setup(bot):
    bot.add_cog(PokemonCog(bot))
