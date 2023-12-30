import dotenv
from interactions import *
from discord import Status, Activity, Game
from time import sleep
from asyncio import TimeoutError
import os
from interactions.api.events import Component
import random
import json
import sqlite3
from googleapiclient.discovery import build


api_key="AIzaSyDukbl24jfE7XqY5gH4TbgdTPr_1w0dquM"
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        balance INTEGER
    )
''')
conn.commit()

# intents 
intents = Intents.ALL
intents.members = True
dotenv.load_dotenv()

bot = Client(token=os.getenv("DISCORD_TOKEN"), intents=intents)



@listen()
async def on_ready():
    print(f'Bot is ready.')
    await bot.change_presence(activity=Game(name="with your mom"))


@slash_command(
    name="help",
    description="Show available commands"
)
async def help_command(ctx: SlashContext):
    await ctx.defer()
    help_text = """
This is an example help text.
    """

    await ctx.send(embed=Embed(title="Help", description=help_text, color=0x73a66e))

# create a command that plays rock paper scissors
@slash_command(
    name="rps",
    description="Play rock paper scissors"
)
async def rps_command(ctx: SlashContext):
    await ctx.defer()
    components1: list[ActionRow] = [
    ActionRow(
        Button(
            style=ButtonStyle.RED,
            label="Rock",
            custom_id="rock"
        ),
        Button(
            style=ButtonStyle.GREEN,
            label="Paper",
            custom_id="paper"
        ),
        Button(
            style=ButtonStyle.BLUE,
            label="Scissors",
            custom_id="scissors"
        )
    )
    ]

    description = "Choose your weapon"

    await ctx.send(embed=Embed(title="Your choice", description=description, color=0x32bb5a), components=components1)
    
@listen()
async def on_component_rps(event: Component):
    ctx = event.ctx

    bot_choice = random.choice(["rock", "paper", "scissors"])


    match ctx.custom_id:
        case "rock":
            if bot_choice == "rock":
                await ctx.edit_origin(embed=Embed(title="Draw!", description="We both chose rock", color=0x32bb5a))
            elif bot_choice == "paper":
                await ctx.edit_origin(embed=Embed(title="You lost!", description="You chose rock, I chose paper", color=0x32bb5a))
            elif bot_choice == "scissors":
                await ctx.edit_origin(embed=Embed(title="You won!", description="You chose rock, I chose scissors", color=0x32bb5a))
        case "paper":
            if bot_choice == "rock":
                await ctx.edit_origin(embed=Embed(title="You won!", description="You chose paper, I chose rock", color=0x32bb5a))
            elif bot_choice == "paper":
                await ctx.edit_origin(embed=Embed(title="Draw!", description="We both chose paper", color=0x32bb5a))
            elif bot_choice == "scissors":
                await ctx.edit_origin(embed=Embed(title="You lost!", description="You chose paper, I chose scissors", color=0x32bb5a))
        case "scissors":
            if bot_choice == "rock":
                await ctx.edit_origin(embed=Embed(title="You lost!", description="You chose scissors, I chose rock", color=0x32bb5a))
            elif bot_choice == "paper":
                await ctx.edit_origin(embed=Embed(title="You won!", description="You chose scissors, I chose paper", color=0x32bb5a))
            elif bot_choice == "scissors":
                await ctx.edit_origin(embed=Embed(title="Draw!", description="We both chose scissors", color=0x32bb5a))



@slash_command(
    name="ping",
    description="Ping the bot"
)
async def ping_command(ctx: SlashContext):
    await ctx.defer()
    await ctx.send(embed=Embed(title="Pong!", description=f"Latency: {round(bot.latency * 1000)}ms", color=0x32bb5a))

# now we make some mini games
# create a command that steals a random amount of money from a user
@slash_command(
    name="steal",
    description="Steal a random amount of money from a user"
)
async def steal_command(ctx: SlashContext):
    await ctx.defer()
    
    # get a random user except the bot and the user who used the command
    random_user = random.choice([user for user in ctx.guild.members if user != ctx.author and user != bot.user])

    # insert the user into the database if they don't exist
    cursor.execute(f'SELECT * FROM users WHERE user_id = {random_user.id}')
    if cursor.fetchone() is None:
        cursor.execute(f'INSERT INTO users VALUES ({random_user.id}, 500)')
        conn.commit()

    # get the user's balance
    cursor.execute(f'SELECT balance FROM users WHERE user_id = {random_user.id}')
    random_user_balance = cursor.fetchone()[0]

    # set a random amount to steal
    steal_amount = random.randint(1, random_user_balance)

    # steal the money
    if random_user_balance - steal_amount < 0:
        steal_amount = random_user_balance
        
        cursor.execute(f'UPDATE users SET balance = {random_user_balance - steal_amount} WHERE user_id = {random_user.id}')
        conn.commit()

        # add the money to the user's balance
        cursor.execute(f'SELECT balance FROM users WHERE user_id = {ctx.author.id}')
        user_balance = cursor.fetchone()[0]
        cursor.execute(f'UPDATE users SET balance = {user_balance + steal_amount} WHERE user_id = {ctx.author.id}')
        conn.commit()
        await ctx.send(embed=Embed(title="Steal", description=f"You stole {steal_amount}$ from {random_user.mention}", color=0x32bb5a))

    else:
        cursor.execute(f'UPDATE users SET balance = {random_user_balance - steal_amount} WHERE user_id = {random_user.id}')
        conn.commit()

        # add the money to the user's balance
        cursor.execute(f'SELECT balance FROM users WHERE user_id = {ctx.author.id}')
        user_balance = cursor.fetchone()[0]
        cursor.execute(f'UPDATE users SET balance = {user_balance + steal_amount} WHERE user_id = {ctx.author.id}')
        conn.commit()
        await ctx.send(embed=Embed(title="Steal", description=f"You stole {steal_amount}$ from {random_user.mention}", color=0x32bb5a))


    if random_user_balance == 0:
        await ctx.send(embed=Embed(title="Steal", description=f"You tried to steal from {random_user.mention} but they had no money", color=0x32bb5a))
        return

# create a command that shows you your balance
@slash_command(
    name="balance",
    description="Show your balance"
)
async def balance_command(ctx: SlashContext):
    await ctx.defer()
    cursor.execute(f'SELECT balance FROM users WHERE user_id = {ctx.author.id}')
    user_balance = cursor.fetchone()[0]
    await ctx.send(embed=Embed(title="Balance", description=f"Your balance is {user_balance}$", color=0x32bb5a))

@slash_command(
     name="show",
    description="Tell me what you want to see",
    options=[
        Option(name="query", description="Mot clé de recherche", type=OptionType.STRING)
    ]
)
async def search_command(ctx: SlashContext, query: str):
    await ctx.defer()
    ran = random.randint(0, 9)
    resource = build("customsearch", "v1", developerKey=api_key).cse()
    result = resource.list(
        q=query, cx="63f5afb4f64024385", searchType="image"
    ).execute()

    if "items" in result and result["items"]:
        url = result["items"][ran]["link"]
        embed = Embed(title=f"Résultat de la recherche pour '{query}'")
        embed.set_image(url=url)
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"Aucun résultat trouvé pour '{query}'")




if __name__ == '__main__':

    bot.start()
