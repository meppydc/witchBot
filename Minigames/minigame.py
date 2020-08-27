import discord
import asyncio
from Util import util
from Util import file_manager

from threading import Timer

class Minigame:
    

    def __init__(self, channel, user=None):
        self.name = "Base Minigame"
        self.channel = channel
        self.user = user
        self.finished = False
        self.timer = Timer(120.0, self.timeUp)
        self.timer.start()
        self.start = util.get_time()
        
        

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
        
        if self.user.id == user.id:
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
                
                await self.finish()
                return
            self.resetTimer()
            await self.output(input)
            await self.instruction()

    async def finish(self):
        self.finished = True
        end = util.get_time()
        delta = util.compare_time(self.start, end, 0)
        await self.channel.send(f"You won in {util.secsFormat(delta)}.")

        lb = file_manager.file_to_array("Minigames/" + self.name.lower().replace(" ", "_") + "_leaderboard.txt", False)
        i = 0
        while i < 10:
            if delta < float(lb[i + 10]):
                lb.insert(i + 10, str(delta))
                lb.insert(i, str(self.user))
                await self.channel.send("Updating leaderboard...")
                lb.pop(10)
                lb.pop(20)
                file_manager.array_to_file("Minigames/" + self.name.lower().replace(" ", "_") + "_leaderboard.txt", lb, True)
                break 
            i += 1
        