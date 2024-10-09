#!/usr/bin/python3.11
from Board import Board
from Player import Player

# Game setup
b = Board(10, 4)
username = input('Please enter your name: \n')
p = Player(username)

print('Welcome: ' + p.name)
print(b)

# Player guessing loop
row = 0
col = 0
while row != '' and col != '':
    scoreFromGuess = 0

    try:
        row = input('Please guess row of next treasure (0-9): \n')
        col = input('Please guess column of next treasure (0-9): \n')
        scoreFromGuess = b.pick(int(row), int(col))
    except ValueError:
        row=0
        col=0
        print('Please enter valid integer values')
    except IndexError:
        print('Please enter a number between 0-9')

    if scoreFromGuess != '_':
        p.addscore(int(scoreFromGuess))
        print('Congratualations, you earned: ' + str(scoreFromGuess) + ' points!')
    else:
        print('Close, but no cigar...')

    print(p)
    print(b)

