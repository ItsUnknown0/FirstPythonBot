import discord
from discord.ext import commands

import random
import json

BOT_TOKEN = "token"

bot = commands.Bot(command_prefix="+", intents = discord.Intents.all())

def chatLevels(msg):
    convertedData : dict = {}

    with open('./data.json', 'r') as file:
        data = file.read()
        if not data == "":
            convertedData = json.loads(data)
        else:
            convertedData[msg.author.id] = {
            'Level' : 1,
            'XP' : 0
    }
    
    convertedData[str(msg.author.id)]["XP"] += 1

    if convertedData[str(msg.author.id)]["XP"] >= 2 * convertedData[str(msg.author.id)]["Level"]:
        convertedData[str(msg.author.id)]["XP"] = 0
        convertedData[str(msg.author.id)]["Level"] += 1
        print(msg.author.name + " just leveled up to " + str(convertedData[str(msg.author.id)]["Level"]))
    
    with open('./data.json', 'w') as output:
        json.dump(convertedData, output, indent=2)

@bot.event
async def on_ready():
    print("hopped on the cord")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

@bot.event
async def on_message(msg):
    if msg.author == bot or msg.author.bot:
        return
    
    chatLevels(msg)

@bot.tree.command(name="hi", description="it just says hi to u back")
async def hi(interation: discord.Interaction):
    await interation.response.send_message(f"hi {interation.user.mention}", ephemeral=True)

@bot.tree.command(name="rand_num", description="gives u very big random number")
async def randNum(interation: discord.Interaction):
    await interation.response.send_message(f"yuh {random.randrange(-10000000,10000000)}")

@bot.tree.command(name="get_level", description="get a user's level")
async def get_level(interation: discord.Interaction, member : discord.Member):
    processedData = None
    with open('./data.json', 'r') as file:
        data = file.read()
        processedData = json.loads(data)

    if processedData.get(str(member.id)):
        await interation.response.send_message(f"{member.mention} is level {processedData[str(member.id)]['Level']}!")
    else:
        await interation.response.send_message(f"{member.mention} is level 1!")

bot.run(BOT_TOKEN)
