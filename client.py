# Client Program
import socket
import struct

HOST = ''    # The remote host
PORT = 12345 # The same port as used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))

    # Receive player name length and name
    playerNameLength = struct.unpack('!H', sock.recv(2))[0]
    playerName = sock.recv(playerNameLength).decode()
    print(f'Playername: {playerName}')

    while True:
        # Input guess from player
        playerRow = input(f'{playerName} Guess a row: ')
        playerCol = input(f'{playerName} Guess a column: ')

        playerGuess = str(playerCol) + str(playerRow)
        sock.sendall(bytes.fromhex(playerGuess))

        playerScore = struct.unpack('!HH', sock.recv(4))[0]
        print(f'Player score: {playerScore}')
