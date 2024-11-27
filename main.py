from typing import Optional, Literal

import discord
from discord.ext import commands
import os
import subprocess
from rcon.source import Client

DISCORD_TOKEN = os.getenv("BOT_TOKEN")

if DISCORD_TOKEN is None:
    print("DISCORD_TOKEN environment variable not found.")
    exit(1)

# Rest of the code

intents = discord.Intents.all()
intents.typing = False
intents.presences = False

bot = commands.Bot(intents=intents, command_prefix="!")
tree = bot.tree


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} ({bot.user.id})")
    print("------")


@tree.command(name="ping", description="ping! Pong!")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!", ephemeral=True)


# Umbra's sync command
# Source: https://about.abstractumbra.dev/discord.py/2023/01/29/sync-command-example.html
@bot.command()
@commands.guild_only()
@commands.is_owner()
async def sync(ctx: commands.Context, guilds: commands.Greedy[discord.Object],
               spec: Optional[Literal["~", "*", "^"]] = None) -> None:
    if not guilds:
        if spec == "~":
            synced = await bot.tree.sync(guild=ctx.guild)
        elif spec == "*":
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await bot.tree.sync(guild=ctx.guild)
        elif spec == "^":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        else:
            synced = await ctx.bot.tree.sync()

        await ctx.send(
            f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
        )
        return

    ret = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            ret += 1

    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")


@tree.command(name="free", description="show memory information")
async def memory(interaction: discord.Interaction):
    sub = subprocess.run(["free", "-h"], stdout=subprocess.PIPE)
    print(sub.stdout.decode())
    await interaction.response.send_message(sub.stdout.decode(), ephemeral=True)


@tree.command(name="avg", description="show load average")
async def avg(interaction: discord.Interaction):
    sub = subprocess.run(["cat", "/proc/loadavg"], stdout=subprocess.PIPE)
    print(sub.stdout.decode())
    await interaction.response.send_message(sub.stdout.decode(), ephemeral=True)


@tree.command(name="add_whitelist")
async def add_white_list(interaction: discord.Integration, user: str):
    sub = subprocess.run(["docker", "exec minecraft-mc-1", "rcon-cli", "whitelist", "add", user],
                         stdout=subprocess.PIPE)
    await interaction.response.send_message(f"Added {user} to whitelist log:{sub.stdout.decode()}", ephemeral=True)

@tree.command(name="Show Joined Users")
async def user_list(interaction: discord.Integration):
    sub = subprocess.run(["docker", "exec minecraft-mc-1", "rcon-cli", "list"],
                         stdout=subprocess.PIPE)
    await interaction.response.send_message(f"Playing Users: \n {sub.stdout.decode()}", ephemeral=True)

bot.run(DISCORD_TOKEN)
