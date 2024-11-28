class Player:
    # Assigning correct values to members.
    def __init__(self, name):
        self.name = name
        self.score = 0

    # Adds a new score to exisitng score.
    def addscore(self, newScore):
        self.score += newScore

    # Gets the current player score.
    def getscore(self):
        return self.score

    def __str__(self):
        playerString = ''
        playerString += 'Player Name: ' + self.name + '\n' + 'Score: ' + str(self.score)
        return playerString
