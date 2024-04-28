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
    print("Syncing commands")
    await tree.sync()
    print("Synced commands")


@tree.command(name="ping", description="ping! Pong!")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!", ephemeral=True)
    print("sync")
    await tree.sync(guild=discord.Object(id=911047487144484947))
    print("synced")
    await tree.sync()
    print("super sync")


@tree.command(name="sync", description="sync command")
async def sync(interaction: discord.Interaction):
    await interaction.response.send_message("Starting Sync", ephemeral=True)
    print("sync")
    await tree.sync(guild=discord.Object(id=911047487144484947))
    print("synced")
    await tree.sync()
    print("super sync")


@tree.command(name="free", description="show memory information")
async def memory(interaction: discord.Interaction):
    sub = subprocess.run(["free", "-h"], stdout=subprocess.PIPE)
    print(sub.stdout.decode())
    await interaction.response.send_message(sub.stdout.decode(), ephemeral=True)


@tree.command(name="avg", description="show load average")
async def memory(interaction: discord.Interaction):
    sub = subprocess.run(["cat", "/proc/loadavg"], stdout=subprocess.PIPE)
    print(sub.stdout.decode())
    await interaction.response.send_message(sub.stdout.decode(), ephemeral=True)


@tree.command(name="add_whitelist")
async def add_white_list(interaction: discord.Integration, user: str):
    sub = subprocess.run(["docker", "exec minecraft_mc_1", "rcon-cli", "whitelist", "add", user],
                         stdout=subprocess.PIPE)
    await interaction.response.send_message(f"Added {user} to whitelist log:{sub.stdout.decode()}", ephemeral=True)


bot.run(DISCORD_TOKEN)
