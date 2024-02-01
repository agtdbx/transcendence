import asyncio
from pong_server.ws_game_server import start_game_thread

# List of game server
# List : [server running, port] ; if thread is False, the server is unused
game_servers = [
    [False, 8766],
    # [False, 8767],
    # [False, 8768],
    # [False, 8769],
    # [False, 8770]
]

number_game_servers = 1
# number_game_servers = 5

number_game_servers_free = 1
# game_servers_free = 5


def is_game_server_free():
    global number_game_servers_free
    return (number_game_servers_free != 0)


def create_new_game(map_id : int,
                    power_up_enable : bool,
                    team_left:list[int],
                    team_right:list[int]):
    global number_game_servers_free

    for i in range (number_game_servers):
        if game_servers[i][0] == False:
            game_servers[i][0] = True

            # Create game server thread ^^
            asyncio.create_task(start_game_thread(
                                game_servers[i][1],
                                map_id, power_up_enable,
                                team_left, team_right,
                                game_servers[i]))

            number_game_servers_free -= 1
            return i, game_servers[i][1]

    return None
