#!/usr/bin/python3.11
import struct
from Board import Board
from Player import Player
from asyncio import run, start_server, StreamReader, StreamWriter

# Game board setup.
boardSize = 10
b = Board(boardSize, 4)

# TCP Server variables.
HOST = '127.0.0.1'
PORT = 12345

# Player objects.
players = [Player('One'), Player('Two')]
connected_clients = []

# Asyncio.
async def handle_client(reader: StreamReader, writer: StreamWriter, player: Player) -> None:
    addr = writer.get_extra_info('peername')
    print('Client:', addr)
    print(f"{player.name}")

    while True:
        data = await reader.read(1) # Read 1 byte.
        if not data: # client disconnected.
            print(f"{player.name} disconnected")
            break

        # Process player guess.
        s = data[0] # Get the integer at index 0 within the bytes object.
        dataX, dataY = s & 0b00001111, (s >> 4) & 0b00001111
        print(f"Player: {player.name}")
        print(f"Score: {player.score}")
        print(f'Last guess made: |X: {dataX}, (0x{dataX:X})| |Y: {dataY}, (0x{dataY:X})|')
        print(b)

        # Check for out-of-bounds.
        if not (0 <= dataX < boardSize and 0 <= dataY < boardSize):
            print(f"{player.name} made an out-of-bounds guess, closing connection.")
            break

        # Game logic.
        player.addscore(b.pick(dataX, dataY))

        # Send player score.
        score_message = struct.pack('!HH', player.score, 0)
        writer.write(score_message)
        await writer.drain()  # Ensure the data is sent.

    # Remove the client from the list of connected clients. Reference is not removed automatically.
    if writer in connected_clients:
        connected_clients.remove(writer)

    # Close client connection.
    writer.close()
    await writer.wait_closed()

async def echo(reader: StreamReader, writer: StreamWriter) -> None:
    # Assign player
    if len(connected_clients) < len(players):
        player = players[len(connected_clients)]
        connected_clients.append(writer)

        # Send player name length, and name.
        writer.write(struct.pack('!H', len(player.name)))
        await writer.drain()
        writer.write(player.name.encode())
        await writer.drain()

        # Now handle the client in the handle_client coroutine.
        await handle_client(reader, writer, player)
    else:
        # Close connection if more than two players.
        writer.close()
        await writer.wait_closed()

async def main() -> None:
    server = await start_server(echo, HOST, PORT)
    print(f'Server started on {HOST}:{PORT}')
    async with server:
        await server.serve_forever()

run(main())