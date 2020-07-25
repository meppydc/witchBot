import sys
import json
import requests
import discord
import asyncio

from random import choice
from threading import Timer
from datetime import timedelta

from Minigames import minigame
from Minigames import bullsandcows

import util

with open('keys.json', 'r') as read_file:
    keys = json.load(read_file)
    TOKEN = keys["TOKEN"]   
    OWNER = keys["OWNER"]
    PREFIX = keys["PREFIX"]
    PLEN = keys["PLEN"]
    read_file.close()



status = [

"Puyo Puyo (1992)",
"Puyo Puyo Tsu",
"Puyo Puyo Box",
"Puyo Puyo Sun",
"Puyo Puyo~n",
"Minna de Puyo Puyo",
"Puyo Puyo 7",
"Puyo Puyo!! 20th Anniversary",
"Puyo Puyo Tetris",
"Puyo Puyo Chronicle",
"Puyo Puyo eSports",

"Madou Monogatari 3",
"Madou Monogatari: ARS",
"Madou Monogatari I (Mega Drive)",
"Madou Monogatari (Saturn)",
"Madou Monogatari: Hanamaru Dai Youchienji",
"Madou Monogatari: Tower of the Magician",

"Nazo Puyo: Arle's Roux",
"Super Nazo Puyo: Rulue's Roux",
"PuyoLympic",
"Comet Summoner",
"Puyo Puyo!! Quest",
"Puyo Puyo!! Quest Arcade",
"Puyo Puyo!! Touch",

"Tax Fraud"

]

witchEmotes = [

"<:witchFraud:729928591244263476>",
"<:witchWtf:729928591382544436>",
"<:witchWink:729928591399321632>",
"<:witchlol:729928591399452674>",
"<:witchHappy:729928591420293151>",
"<:witchPissed:729928591613231155>",
"<:witchYay:729928591617294427>",
"<:witchScream:729928591663562824>",
"<:witchSmile:729928591743254608>",
"<:witchSmug:729928591785328680>",
"<:witchHmm:729928591881535521>",
"<:witchShock:729928592430989316>",
"<:witchYikes:729928592930373732>",
"<:witchYes:729928592984637531>",
"<:witchHurt:729928593462788107>",
"<:witchThink:730491882916020315>"

]

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
        #conveniently doesn't allow commands to work in dms LOL
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
    
    if hasWord("witch"):
        await message.add_reaction(choice(witchEmotes))


    if minigames.get(channel.id) and not minigames.get(channel.id).finished:
        game = minigames.get(channel.id)
        if game.validUser(author.id):
            await game.process(message.content)

    if not message.content.startswith(PREFIX):
        return
    command = command[PLEN:]

    if command == ('test'):
        await channel.send('test')
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


async def statusChange():
    await client.change_presence(activity= discord.Game(choice(status)))

client.run(TOKEN)