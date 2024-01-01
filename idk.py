import discord
from discord.ext import commands
from token import *


bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
@bot.event
async def on_ready():
    print("s'est bien connécté")



@bot.command()
async def add(ctx: commands.Context, a : int , b : int):
    return await ctx.send(str(a + b))

@bot.command()
async def hey(ctx: commands.Context, member : discord.Member):
    return await ctx.send(f"hey{member.name} ! ")

@bot.command()
async def supprimer(ctx, nombre: int):
    await ctx.channel.purge(limit=nombre+1)

@bot.command()
async def mute(ctx, member: discord.Member, *, reason=None):
    role = discord.utils.get(ctx.guild.roles, name='Muted')
    if not role:
        role = await ctx.guild.create_role(name='Muted')
        for channel in ctx.guild.channels:
            await channel.set_permissions(role, send_messages=False)
    await member.add_roles(role, reason=reason)
    await ctx.send(f'{member.mention} a été muté pour la raison suivante : {reason}')



@bot.command()
async def unmute(ctx, member: discord.Member):
    if not ctx.author.guild_permissions.mute_members:
        await ctx.send("Vous n'avez pas la permission d'unmute des membres.")
        return

    if member == ctx.author:
        await ctx.send("Vous ne pouvez pas vous unmute vous-même.")
        return

    if member == bot.user:
        await ctx.send("Je ne peux pas me unmute moi-même.")
        return

    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not muted_role:
        await ctx.send("Il n'y a pas de rôle 'Muted' sur ce serveur.")
        return

    if muted_role not in member.roles:
        await ctx.send(f"{member.mention} n'est pas mute.")
        return

    await member.remove_roles(muted_role)
    await ctx.send(f"{member.mention} a été unmute.")





if name == "main" :
    bot.run("TOKEN)
