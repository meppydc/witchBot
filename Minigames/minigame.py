import discord
import asyncio
import util

from threading import Timer

class Minigame:
    

    def __init__(self, channel, user=None):
        self.name = "Base Minigame"
        self.channel = channel
        self.user = user
        self.finished = False
        self.timer = Timer(120.0, self.timeUp)
        self.timer.start()
        

    def timeUp(self):
        self.finished = True

    def resetTimer(self):
        self.timer.cancel()
        self.timer = Timer(120.0, self.timeUp)
        self.timer.start()
        print("reset timer")

    def validUser(self,user):
        if not self.user:
            return True
        
        if self.user == user:
            return True
        return False

    def validate(self, input):
        if input:
            return True
    
    async def instruction(self):
        await self.channel.send("Type in an input")

    async def output(self, input):
        await self.channel.send("The input was " + input)

    async def process(self, input):
        if self.validate(input):
            if input == "h":
                await self.channel.send("You won.")
                self.finished = True
                return
            self.resetTimer()
            await self.output(input)
            await self.instruction()

    