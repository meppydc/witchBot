from Util import util
import json
with open('keys.json', 'r') as read_file:
    PREFIX = json.load(read_file)['PREFIX']
from functools import reduce



helpMessages = ["Try running the command", "That's for you to see with your own eyes", "It's up to you to find out", "It's a secret", ":o"]


class Command:

    def __init__(self, name, description, example):
        # (string, string, string)
        self.name = name
        self.arguments = []
        self.description = description
        self.example = example
        
    def add_arg(self, argname, argdesc):
        self.arguments.append([argname,argdesc])


    def info(self):
        
        fields = [
            ("Parameter", reduce(lambda x,y: x + "\n" + f"`{y[0]}`" , self.arguments , ""), True),
            ("Usage", reduce(lambda x,y: x + "\n" + y[1] , self.arguments , "") , True)
        ]


        embed = util.created_embed(
            title= self.name,
            description="{}\n\n{}".format(self.description.capitalize(), reduce(lambda x,y:x + f'\n`{PREFIX}{y}`',self.example,"**Examples:**")),
            fields = fields if fields[0][1] else None,
            author= ("Command", "", "")
            #footer= "[] - list, <> - single parameter, () - default value"
            
        )
        return embed

testCommand = Command("test", "for testing purposes abcdefghijklmnopqrstuvwxyz1234567890", ["test arg1","test arg1 arg2"])
testCommand.add_arg("<arg1>", "argument 1")
testCommand.add_arg("[arg2]", "argument 2")

helpCommand = Command("help", "if you read this you know how to use this", ["help help","help pepega"])
helpCommand.add_arg("<command>", "a command to learn more about")

bulluCommand = Command("bullu", f"Starts a bulls and cows game. Exit using {PREFIX}exit\n2 minute inactivity timer.\nAlias: bullus", ["bullu"])

exitCommand = Command("exit","Exit out of a running minigame.",["exit"])



commands = {
    "test": testCommand,
    "help": helpCommand,

    "bullu": bulluCommand,
    "exit": exitCommand
}