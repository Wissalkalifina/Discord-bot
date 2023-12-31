import discord
from discord.ext import commands
import os
from googleapiclient.discovery import build
import random

intents = discord.Intents.default()
intents.message_content = True  # Définissez message_content sur True pour permettre la gestion des messages

client = commands.Bot(command_prefix="$", intents=intents)
api_key="AIzaSyDukbl24jfE7XqY5gH4TbgdTPr_1w0dquM"



@client.event
async def on_ready():
        print(f'Connecté en tant que {client.user.name}')
        print('Bot prêt!')

#recherche sur google d'un mot donner

@client.command(aliases=["show"])
async def showpic(ctx, *, search):
    ran = random.randint(0, 9)
    resource = build("customsearch", "v1", developerKey=api_key).cse()
    result = resource.list(
        q=f"{search}", cx="63f5afb4f64024385", searchType="image"
    ).execute()
    url = result["items"][ran]["link"]
    embed1 = discord.Embed(title=f"Voici ({search}!) ")
    embed1.set_image(url=url)
    await ctx.send(embed=embed1)


# Lancement du bot
client.run('TOKEN')
