import discord
from discord.ext import commands
import os
import subprocess

DISCORD_TOKEN = os.getenv("BOT_TOKEN")

if DISCORD_TOKEN is None:
    print("DISCORD_TOKEN environment variable not found.")
    exit(1)

# Rest of the code

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

@client.event
async def on_ready():
    print(f"Logged in as {client.user.name} ({client.user.id})")
    print("------")
    await tree.sync()

@tree.command(name = "ping", description="ping! Pong!")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!", ephemeral=True)

@tree.command(name="add_whitelist")
async def add_white_list(interaction: discord.Integration, user: str):
    await interaction.response.send_message(f"Added {user} to whitelist")
    


client.run(DISCORD_TOKEN)