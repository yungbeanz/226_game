from django.test import TestCase
import sys
sys.path.append("..")
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
        self.assertEqual(len(b.board), 100)

    def test_score_update(self):
        # Test for functionality where a player picks a tile and their score updates
        # Example test to simulate score update functionality
        response = self.client.get(reverse('pick', args=["One", 0, 0]))  # Pick the tile at (0, 0) for player "One"

        # Check the score update based on the expected behavior
        from game.views import playerOne, playerTwo
        self.assertGreater(playerOne.score, 0)  # Check that playerOne's score increased after the pick
