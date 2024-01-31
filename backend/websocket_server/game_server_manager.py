# List of game server
# List : [thread, port] ; if thread is None, the server is unused
game_servers = [
    [None, 8766],
    # [None, 8767],
    # [None, 8768],
    # [None, 8769],
    # [None, 8770]
]

number_game_servers = 1
# number_game_servers = 5

number_game_servers_free = 1
# game_servers_free = 5


def create_new_game(map_id : int, power_up_enable : bool):
    global number_game_servers_free
    if number_game_servers_free == 0:
        return None

    for i in range (number_game_servers):
        if game_servers[i][0] == None:
            # Create game server thread ^^
            number_game_servers_free -= 1
            return i, game_servers[i][1]

    return None
