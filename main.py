#!/usr/bin/python3.11
import struct
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from Board import Board
from Player import Player
from threading import Semaphore, Thread

# Game board setup.
boardSize = 10
b = Board(boardSize, 4)

# TCP Server variables.
HOST = ''
PORT = 12345

# Variables for threads, Player objects.
thread_list = []
players = [Player('One'), Player('Two')]
num = 0
lock = Semaphore()

# Function each client thread will run.
# Contains logic for computing user input over the network to interact with the gameboard.
# Also contains logic for checking client connection, assigning Player objects, and assigning
# these player objects to each client connection.
def handle_client(sc):
    global num
    localNumMemory = num

    # Player assignment logic.
    with lock:
        player = players[num]
        num+=1
    sc.sendall(struct.pack('!H', len(player.name)))
    print(struct.pack('!H', len(player.name)))
    sc.sendall(player.name.encode('utf-8'))

    # Client network communication logic.
    with sc:
        print('Client:', sc.getpeername())
        while True:
            # Receive a bytes object from client consisting of player's guess.
            s = b''
            while len(s) < 1:
                s += sc.recv(1)
                if len(s) == 0: # End client connection if no data is received.
                    with lock:
                        thread_list.remove(thread_list[localNumMemory])
                        num -=1
                    return

            # Process player guess.
            s = s[0] # Get the integer at index 0 within the bytes object.
            dataX, dataY = s & 0b00001111, (s >> 4) & 0b00001111
            print(f'Player guess: X={dataX} (0x{dataX:X}), Y={dataY} (0x{dataY:X})')

            # Check for out-of-bounds, if there is an out-of-bounds, end client connection.
            if not (0 <= dataX < boardSize and 0 <= dataY < boardSize):
                print('Received out-of-bounds guess, closing connection.')
                with lock:
                    thread_list.remove(thread_list[localNumMemory])
                    num -= 1
                return

            # Game logic.
            player.addscore(b.pick(dataX, dataY))

            # Send player score.
            t = struct.pack('!HH', player.score, 0)
            sc.sendall(t)

            # Print board.
            print(b)

# Create network socket.
with socket(AF_INET, SOCK_STREAM) as sock:
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    sock.listen(2) # Allow up to 2 connections.
    print('Server:', sock.getsockname())

    while True:
        # Create new threads for new client connections, if there are available spots.
        if len(thread_list) < 2:
            sc, _ = sock.accept()  # Accept connection.

            # Creating a new thread for each client connection.
            newThread = Thread(target=handle_client, args=(sc,))
            thread_list.append(newThread) # Append thread to list of client threads.
            newThread.start() # Execute the thread.

