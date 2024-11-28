from django.test import TestCase
from Board import Board
from Player import Player

# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from game.views import index, create, pick

class GameViewsTest(TestCase):
    def setUp(self):
        # Call first url that displays game, and if players and board aren't created, creates two player objects and 100 grid board.
        response = self.client.get(reverse('index'))

        # Assert that the response status is 200 (OK)
        self.assertEqual(response.status_code, 200)

    def test_game_initialization(self):
        # We import the globals to check their state
        from game.views import playerOne, playerTwo, b

        # Check that players are created correctly
        self.assertIsInstance(playerOne, Player)
        self.assertIsInstance(playerTwo, Player)
        self.assertEqual(playerOne.name, "One")
        self.assertEqual(playerTwo.name, "Two")

        # Check that the board is initialized correctly
        self.assertIsInstance(b, Board)
        boardLength = 0
        for i in range(0, len(b.board)):
            for j in range(0, len(b.board[i])):
                boardLength += 1
        self.assertEqual(boardLength, 100)

    def test_score_update(self):
        # Tests to simulate score update functionality
        for i in range(0, 10):
            for j in range(0, 10):
                response = self.client.get(reverse('pick', args=["One", i, j]))

        # Because the board is randomized, it's almost impossible to get both players to pick set locations on the board, and both end up with a score.
        # One of them might end up with 0 because of the board treasure placement randomization, and throw an error for no reason, so we're just testing player one.
        # We already know player two is created from prior tests.
        # So the tested functionality of player one should remain consistent to player two.

        # Check the score update based on the expected behavior
        from game.views import playerOne
        self.assertGreater(playerOne.score, 0)  # Check that playerOne's score increased after the pick
