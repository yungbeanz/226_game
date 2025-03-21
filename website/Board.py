import random

class Board:

    # Assigning correct values to members.
    def __init__(self, n, t):
        self.boardSize = n
        self.treasureSize = t
        self.treasures = []
        self.board = []

        # Error handling before program continues.
        if not isinstance(self.boardSize, int) or not isinstance(self.treasureSize, int):
            raise TypeError('Board only takes two integer parameters.')
        if self.boardSize <= 0 or self.treasureSize <= 0:
            raise ValueError('Board parameters must be positive integers.')

        # Error handling to make sure that treasure size is smaller than board size.
        if self.treasureSize > self.boardSize:
            raise Exception('Please make sure the treasure is the same size, or smaller than the board size.')

        # Call the function that creates the gameboard.
        self.createGameBoard()

    # Initializing gameboard values - there must be 1 treasure labelled 1,
    # t treasures labelled t.
    # Treasures are placed randomly, except each treasure sharing the same label are connected vertically,
    # or horizontally, possibly wrapping around the edges of the board.
    def createGameBoard(self):

        # Initializing board array.
        for i in range(0, self.boardSize):
            self.board.append([])
            for j in range(0, self.boardSize):
                self.board[i].append('_')

        # Initializing array of treasures.
        for i in range(0, self.treasureSize):
            self.treasures.append([])
            for j in range(0, i+1):
                self.treasures[i].append([])
                self.treasures[i][j] = str(i+1)

        # Randomly assign the treasure values to positions on the board.
        # First treasures are placed randomly, every following treasure checks if there is treasure in its position to be placed.
        i = 0
        while i < self.treasureSize:
            randomRow = random.randint(0, self.boardSize - 1)
            randomColumn = random.randint(0, self.boardSize - 1)
            # Check if positions are empty, upwards, right, left, then down. Then assign treasures this direction.
            if self.checkforopensurroundings(randomRow, randomColumn, i):
                i += 1
                self.__str__()
            else:
                continue

        # Call the function that creates the string version of the gameboard.
        self.__str__()

    # Checks for open surroundings, returns false if there are no clear paths, returns true if there is.
    def checkforopensurroundings(self, row, column, i):
        openSpots = True

        if self.board[row][column] == '_':

            if (column - i) > 0:
                for j in range(0, i + 1):
                    if self.board[row][column - j] == '_':
                        continue
                    else:
                        openSpots = False
                        break
                if openSpots:
                    for j in range(0, i + 1):
                        self.board[row][column - j] = str(self.treasures[i][j])

            elif (row + i) < self.boardSize:
                for j in range(0, i + 1):
                    if self.board[row + j][column] == '_':
                        continue
                    else:
                        openSpots = False
                        break
                if openSpots:
                    for j in range(0, i + 1):
                        self.board[row + j][column] = str(self.treasures[i][j])

            elif (row - i) > 0:
                for j in range(0, i + 1):
                    if self.board[row - j][column] == '_':
                        continue
                    else:
                        openSpots = False
                        break
                if openSpots:
                    for j in range(0, i + 1):
                        self.board[row - j][column] = str(self.treasures[i][j])

            elif (column + i) < self.boardSize:
                for j in range(0, i + 1):
                    if self.board[row][column + j] == '_':
                        continue
                    else:
                        openSpots = False
                        break
                if openSpots:
                    for j in range(0, i + 1):
                        self.board[row][column + j] = str(self.treasures[i][j])

        else:
            openSpots = False

        return openSpots

    # Locates a position on the gameboard, sets the position to '_' and returns that value in that position
    def pick(self, row, col):
        treasureValue = self.board[row][col]
        if treasureValue == '_':
            treasureValue = 0
        self.board[row][col] = '_'

        return int(treasureValue)

    # Prints the gameboard
    def __str__(self):
        gameboardStr = ''

        for i in range(0, self.boardSize):
            for j in range(0, self.boardSize):
                gameboardStr += str(self.board[i][j]) + ' '
            gameboardStr += '\n'

        return gameboardStr


