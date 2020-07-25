import discord
import asyncio

class Minigame:
    

    def __init__(self, channel, user=None):
        self.name = "Base Minigame"
        self.channel = channel
        self.user = user
        self.finished = False
        

    def validUser(self,user):
        if not self.user:
            return True
        
        if self.user == user:
            return True
        return False

    def validate(self, input):
        if input:
            return True

    async def output(self, input):
        await self.channel.send("The input was " + input)

    async def process(self, input):
        if self.validate(input):
            if input == "h":
                await self.channel.send("You won.")
                self.finished = true
                return
            await self.output(input)

    