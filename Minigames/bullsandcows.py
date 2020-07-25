from Minigames import minigame

import random

class BullsAndCows(minigame.Minigame):

    def __init__(self, channel, user=None):
        super().__init__(channel, user=user)
        self.name = "Bullus and Cowards"
        self.secret = list('1234567890')
        while len(self.secret) > 4:
            self.secret.remove(random.choice(self.secret))
        random.shuffle(self.secret)
        self.secret = ''.join(self.secret)
        self.guesses = 0

    def validate(self, input):
        if not input.isnumeric():
            return 0
        if len(input) != 4:
            return 2
        return 1

    async def output(self,bulls,cows):
        await self.channel.send(f"{bulls} bullus and {cows} cowards")

    async def process(self, input):
        inputCode = self.validate(input)

        if inputCode == 1:
            guess = input
            bulls = cows = 0
            for i in range(4):
                if guess[i] in self.secret:
                    if guess[i] == self.secret[i]:
                        bulls += 1
                    else:
                        cows += 1
            self.guesses += 1
            if bulls == 4:
                await self.channel.send(f"The number was {self.secret}! You guessed it in {self.guesses} tries. I wasn't too tough, was I?")
                self.finished = True
                return
            await self.output(bulls,cows)
        elif inputCode == 2:
            await self.channel.send("You're useless!")
