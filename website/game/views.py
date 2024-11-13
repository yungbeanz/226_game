from django.shortcuts import render
from django.http import HttpResponse
import sys
sys.path.append("..")
from Board import Board
from Player import Player

# Initializing variables, the create function must be called prior to any player choosing a location.
# It seems that for some reason when the /create url browser is left open, when the /pick url is called,
# it resets the board.
playerOne = ''
playerTwo = ''
b = ''

def index(request):
        global playerOne
        global playerTwo
        global b

        return HttpResponse(f'<div style="display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center"><div style="background-color: orange; font-size: 35px; color: white; style: bold;">{playerOne} Score: {playerOne.score}</div><div style="font-size: 35px; background-color:red; color: white; style: bold;">{playerTwo} Score: {playerTwo.score}</div><div style="font-size: 25px; width: 10%; align-text: center;">{b}</div></div>')


def greet(request, name):
        return HttpResponse(f'Hello {name}')

def create(request):
        global playerOne
        global playerTwo
        global b

        playerOne = Player("One")
        playerTwo = Player("Two")
        b = Board(10, 4)
        return HttpResponse(f'<div style="display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center"><div style="background-color: orange; font-size: 35px; color: white; style: bold;">{playerOne} Score: {playerOne.score}</div><div style="font-size: 35px; background-color:red; color: white; style: bold;">{playerTwo} Score: {playerTwo.score}</div><div style="font-size: 25px; width: 10%; align-text: center;">{b}</div></div>')


def pick(request, player, x, y):
        global playerOne
        global playerTwo
        global b
        score = b.pick(int(x), int(y))

        if player == "One":
                playerOne.addscore(score)
        if player == "Two":
                playerTwo.addscore(score)
        return HttpResponse(f'<div style="display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center"><div style="background-color: orange; font-size: 35px; color: white; style: bold;">{playerOne} Score: {playerOne.score}</div><div style="font-size: 35px; background-color:red; color: white; style: bold;">{playerTwo} Score: {playerTwo.score}</div><div style="font-size: 25px; width: 10%; align-text: center;">{b}</div></div>')

