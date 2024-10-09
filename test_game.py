#!/usr/bin/python3.11
from Player import Player

def test_player():
    p = Player("TestPlayer")

    # Testing Player object creation.
    assert p.name == "TestPlayer"
    assert p.score == 0

    # Testing Player addscore and getscore methods.
    p.addscore(10)
    assert p.getscore() == 10
    p.addscore(5)
    assert p.getscore() == 15

    # Testing Player __str__ method.
    assert p.__str__() == 'Player Name: TestPlayer\nScore: 15'

import pytest
from Board import Board

def test_board():
    # Testing Board constructor.
    with pytest.raises(TypeError, match='Board only takes two integer parameters.'):
        b = Board(5.5, 3.5)
    with pytest.raises(ValueError, match='Board parameters must be positive integers.'):
        b = Board(-5, -2)
    with pytest.raises(Exception, match='Please make sure the treasure is the same size, or smaller than the board size.'):
        b = Board(3,5)

    # Testing checkForOpenSurroundings method.
    b = Board(2, 1)
    assert b.checkforopensurroundings(1, 1, 0) in [True, False]

    # Testing createGameBoard method.
    b = Board(2, 1)
    assert b.createGameBoard() == '1_\n__' or '_1\n__' or '__\n1_' or '__\n_1'

    b = Board(30, 30)
    for i in range(0, b.boardSize):
        for j in range(0, b.boardSize):
            assert isinstance(b.board[i][j], str)

    # Testing pick method.
    b = Board(2, 1)
    assert b.pick(0,0) == '_' or '1'

    # Testing Board __str__ method.
    b = Board(2, 1)
    assert b.__str__() == '1_\n__' or '_1\n__' or '__\n1_' or '__\n_1'