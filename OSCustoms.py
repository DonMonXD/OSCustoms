import os

from random import choice

import csv
import discord
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN_OS_CUSTOMS')
gamers = []
gamer_file = "D:/OSCustoms/gamers.txt"
map_names = []
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
bot_id = 1133791271668945087
debug_id = 1144988486609416262
aimi_tank = "<:Tank_Aimi:1144996335251107931>"

def read_map_names():
    with open("MapNames.txt") as map_name_csv:
        reader = csv.reader(map_name_csv)
        for map_names_reader in reader:
            for map_name in map_names_reader:
                map_names.append(map_name)

@bot.event
async def on_ready():
    read_map_names()
    print(map_names)
    file = open(gamer_file)
    for line in file:
        if line.startswith("Gamers:"):
            continue
        gamers.append(line.strip())
    file.close()
    await setStatus()

@bot.event
async def on_message(message):
    message_content = message.content.lower()
    if "tank" in message_content  or "aimi" in message_content or "ai.mi" in message_content:
        if message.author.id == bot_id:
            return
        await sendMessage(message.channel.id, aimi_tank)

    await bot.process_commands(message)

@bot.command()
async def addGamers(ctx, *args):
    for arg in args:
        gamers.append(arg)
    await setStatus()
    await sendMessage(ctx.channel.id, "Gamers added")

@bot.command()
async def removeGamers(ctx, *args):
    if len(args) == 0:
        await sendMessage(ctx.channel.id, "removeGamers was called with 0 arguments. Did you mean to call !clearGamers?")
        return
    for arg in args:
        try:
            gamers.remove(arg)
        except ValueError:
            await sendMessage(ctx.channel.id, arg + " is not a gamer currently in the gamer pool.")
    await setStatus()
    await sendMessage(ctx.channel.id, "Gamers removed")

@bot.command()
async def clearGamers(ctx):
    gamers.clear()
    await sendMessage(ctx.channel.id, "Gamers cleared")
    await setStatus()

@bot.command()
async def viewGamers(ctx):
    gamer_list = ""
    for gamer in gamers:
        gamer_list += gamer + ", "
    if len(gamer_list) == 0:
        await sendMessage(ctx.channel.id, "No gamers. Try using !addGamers")
        return
    await sendMessage(ctx.channel.id, gamer_list[:len(gamer_list) - 2])

@bot.command()
async def saveGamers(ctx):
    with open(gamer_file, 'w') as fp:
        fp.write("%s\n" % "Gamers:")
        for gamer in gamers:
            # write each item on a new line
            fp.write("%s\n" % gamer)
    await sendMessage(ctx.channel.id, "Gamers saved")


def copyList(listToCopy):
    newList = []
    for item in listToCopy:
        newList.append(item)
    return newList

@bot.command()
async def map(ctx, *args):
    await sendMessage(ctx.channel.id, "Map: " + choice(map_names))


@bot.command()
async def genCustoms(ctx, *args):
    await genCustom(ctx, *args)

@bot.command()
async def genCustom(ctx, *args):
    teams = []
    number_of_teams = 2
    if len(args) == 1:
       number_of_teams = int(list(args).pop())
    for i in range(0, int(number_of_teams)):
        teams.append([])
    random_gamers = copyList(gamers)
    for team in teams:
        while len(team) < 3 and len(random_gamers) > 0:
            gamer = choice(random_gamers)
            team.append(gamer)
            random_gamers.remove(gamer)
    team_count = 1
    for team in teams:
        team_string = listToString(team)
        if team_string == "":
            continue
        await sendMessage(ctx.channel.id, "Team " + str(team_count) + ": " + listToString(team))
        team_count += 1
    await sendMessage(ctx.channel.id, "Map: " + choice(map_names))

def listToString(list) -> str:
    string = ""
    for item in list:
        string += item + ", "
    return string[:len(string) - 2]


async def setStatus():
    await sendMessage(debug_id, "Attempting to set status...")
    gamerString = listToString(gamers)
    if gamerString == "":
        gamerString = " "
    await bot.change_presence(activity=discord.Game(name=gamerString))
    await sendMessage(debug_id, "Status set to: " + listToString(gamers))


async def sendMessage(channel_id, message):
    if not channel_id == debug_id:
        await bot.get_channel(debug_id).send("Attempting to send message to channel with id: " + str(channel_id) +
                                             "\nAttempting to retrieve channel name: " + bot.get_channel(
                                              channel_id).name + "\nMessage contents are: " + message)
    await bot.get_channel(channel_id).send(message)



bot.run(TOKEN)
