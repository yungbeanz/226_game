#!/usr/bin/python3.11
import struct

from Board import Board
from Player import Player
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR

# Board initialization
# Game setup
boardSize = 10
b = Board(boardSize, 4)
username = 'Player1'
p = Player(username)

# Player guessing loop
row = 0
col = 0

# TCP SERVER
BUF_SIZE = 1024
HOST = ''
PORT = 12345

with socket(AF_INET, SOCK_STREAM) as sock: # TCP socket
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # Details later
    sock.bind((HOST, PORT)) # Claim messages sent to port "PORT"
    sock.listen(1) # Server only supports a single 3-way handshake at a time
    print('Server:', sock.getsockname()) # Server IP and port
    while True:
        sc, _ = sock.accept() # Wait until a connection is established
        with sc:
            print('Client:', sc.getpeername()) # Client IP and port
            s = sc.recv(BUF_SIZE)[0] # recvfrom not needed since address known
            dataX = s & 0b00001111
            dataY = (s >> 4) & 0b00001111
            print('Player guess in hexadecimal: X: ' + str(hex(dataX)) + ' Y: ' + str(hex(dataY)) + '\nPlayer guess in decimal: X: ' + str(dataX) +  ' Y: ' + str(dataY))

            # Close connection if values are out of range of board.
            if dataX < 0 or dataX > boardSize or dataY < 0 or dataY > boardSize:
                sc.close()

            # GameLogic
            p.addscore(b.pick(dataX, dataY))

            # Pack playerscore data to unsigned short, with a 0 following, send to connected client, print out original board.
            t = struct.pack('!HH', p.score, 0)
            sc.sendall(t)
            print(t)
            print(b)

            # Close connection after each turn.
            sc.close()
