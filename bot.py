import sys
import json
import requests
import discord
import asyncio

from random import choice
from threading import Timer
from datetime import timedelta
from functools import reduce

from Util import util
from Util import file_manager
from Minigames import minigame
from Minigames import bullsandcows
from help import commands
from help import helpMessages

with open('keys.json', 'r') as read_file:
    keys = json.load(read_file)
    TOKEN = keys["TOKEN"]   
    OWNER = keys["OWNER"]
    PREFIX = keys["PREFIX"]
    PLEN = keys["PLEN"]
    read_file.close()



status = file_manager.file_to_array('Const/status.txt')
witchEmotes = file_manager.file_to_array('Const/witch_emotes.txt')


async def timerMessage(num, channel):
    print(f"{num} second timer")
    if num > 120:
        await channel.send("Leave me alone.")
        return
    await asyncio.sleep(num)
    await channel.send(f"{num} seconds have passed.")

minigames = {}

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    #await asyncTest()  

    await client.change_presence(activity= discord.Game("Tax Fraud"))



@client.event
async def on_message(message):

    if message.author == client.user:
        return
    
    #message_id = message.id
    author = message.author
    channel = message.channel
    try:
        guild = channel.guild
    except:
        pass

    splitString = message.content.split(' ')
    command = splitString[0].casefold()
    args = splitString[1:]

    def hasWord(*words):
        for word in words:
            if message.content.casefold().count(word):
                return True
        return False
    
    if hasWord('@everyone', "@here"):
        await message.add_reaction('<:witchPissed:729928591613231155>')
        await message.add_reaction("💢")
        await message.add_reaction("🏓")
        return

    


    #owner commands
    if author.id == OWNER:

        if command == f'{PREFIX}stop':
            print('close connection')
            await channel.send("I apologize...")
            
            for game in minigames.values():
                game.timer.cancel()
            print("cancel timers?")

            await client.close()
            #sys.exit()
        
        if command == f'{PREFIX}emotes':
            for i in guild.emojis:
                print(f"<:{i.name}:{i.id}")
            return

        if command == f'{PREFIX}content':
            print(message.content)
            await channel.send(message.content[10:])


    if hasWord("witch"):
        await message.add_reaction(choice(witchEmotes))


    if minigames.get(channel.id) and not minigames.get(channel.id).finished:
        game = minigames.get(channel.id)
        if game.validUser(author.id):
            await game.process(message.content)
            if game.finished:
                minigames.pop(channel.id)
                return

    if not message.content.startswith(PREFIX):
        return
    command = command[PLEN:]

    if command == ('help') or command == ('h'):
        await statusChange()
        if len(args) < 1:
            count = len(commands)
            commandNames = list(commands.keys())
            num1 = num2 = int(count/3)
            #scuffed af
            if count % 3 == 1:
                num1 += 1
            elif count % 3 == 2:
                num1 += 1
                num2 += 1

            col1 = commandNames[0:num1]
            col2 = commandNames[num1:num1+num2]
            col3 = commandNames[num1+num2:count]
            fields = [
                ("\u200b",reduce(lambda x,y: x + f"`{y}`\n", col1, ""),True),
                ("\u200b",reduce(lambda x,y: x + f"`{y}`\n", col2, ""),True),
                ("\u200b",reduce(lambda x,y: x + f"`{y}`\n", col3, ""),True)


            ]
            embed = util.created_embed(
                title="Commands",
                description=f"Do `{PREFIX}help <command>` to learn more about it",
                fields=fields)
            await channel.send(embed = embed)

        else:
            try:
                await channel.send(embed = commands[args[0]].info())
            except AttributeError:
                await channel.send(random.choice(helpMessages))
        return

    if command == ('emoji'):
        if len(args) == 1:
            #try:
            await channel.send(witchEmotes[int(args[0])])
            #except:
            #    await channel.send("What a fool.")
        return
    
    if command == ('minigame'):
        if minigames.get(channel.id) and not minigames.get(channel.id).finished:
            await channel.send("A minigame is already in progress!")
        else:
            minigames[channel.id] = minigame.Minigame(channel,author.id)
            await channel.send("Initializing " + minigames.get(channel.id).name)
            await minigames.get(channel.id).instruction()

    if command == ('bullu') or command == ('bullus'):
        if minigames.get(channel.id) and not minigames.get(channel.id).finished:
            await channel.send("A minigame is already in progress!")
        else:
            minigames[channel.id] = bullsandcows.BullsAndCows(channel,author.id)
            await channel.send("Initializing " + minigames.get(channel.id).name)
            await minigames.get(channel.id).instruction()
   
    if command == ('exit'):
        if minigames.get(channel.id):
            game = minigames.get(channel.id)
            if game.validUser(author.id):
                await channel.send("Exitting " + game.name)
                minigames.pop(channel.id)
            elif game.finished:
                await channel.send("Minigame is inactive. Start a new one.")
            else:
                await channel.send("You did not start the minigame.")
        else:
            await channel.send("No minigame in progress.")
        return

    if command == ('timer'):
        if len(args) < 1:
            await channel.send("What a fool.")
        else:
            try:
                args = map(lambda x: int(x), args)
                for num in args:
                    await channel.send(f"Starting {num} second timer.")
                    await timerMessage(num,channel)
            except ValueError:
                await channel.send("What a fool.")

    if command == ('embed'):
        await channel.send(embed=util.created_embed(
            title="embed",
            url="https://leovoel.github.io/embed-visualizer/",
            thumbnail="https://cdn.discordapp.com/emojis/729928591617294427.png",
            description="[embed](https://leovoel.github.io/embed-visualizer/) testing",
            fields=[("hey","you",True),("pepega","peg",True)]
            ))

    if command == ('test'):
        await channel.send('test')
        return


async def statusChange():
    await client.change_presence(activity= discord.Game(choice(status)))

client.run(TOKEN)