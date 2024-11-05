# Client Program
import struct
from asyncio import open_connection, run
from sys import argv

boardSize = 10

# Asyncio client function.
async def client() -> None:
    reader, writer = await open_connection('127.0.0.1', 12345)

    # Read player name length and name from the server.
    player_name_length_data = await reader.readexactly(2)
    player_name_length = struct.unpack('!H', player_name_length_data)[0]
    player_name = await reader.readexactly(player_name_length)
    player_name = player_name.decode()
    print(f'Player name: {player_name}')

    try:
        while True:
            # Input guess from player.
            player_row = input(f'{player_name}, guess a row (0-{boardSize - 1}): ')
            player_col = input(f'{player_name}, guess a column (0-{boardSize - 1}): ')

            # Convert guess to a single byte (assuming 0-15 for each coordinate).
            try:
                data_x = int(player_col) & 0b00001111
                data_y = int(player_row) & 0b00001111
                player_guess = (data_y << 4) | data_x
            except ValueError:
                print("Invalid input. Please enter numbers.")
                continue

            # Send guess to the server.
            writer.write(struct.pack('!H', player_guess))
            await writer.drain()

            # Receive player score from server.
            score_data = await reader.readexactly(4)
            player_score, _ = struct.unpack('!HH', score_data)
            print(f'Player score: {player_score}')

    except Exception as e:
        print(f"Error: {e}")
    finally:
        writer.close()
        await writer.wait_closed()

run(client())