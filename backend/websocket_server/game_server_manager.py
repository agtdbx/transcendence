import os
import asyncio
import sys
import time
import websockets
# from pong_server.ws_game_server import start_game_thread

# List of game server
# List : [server running, port] ; if thread is False, the server is unused
game_servers = [
    [False, 8766],
    # [False, 8767],
    # [False, 8768],
    # [False, 8769],
    # [False, 8770]
]


def is_game_server_free():
    print("\nWS : ALL SERVER :", game_servers, file=sys.stderr)

    for i in range(len(game_servers)):
        if game_servers[i][0] == False:
            return True

    return False


async def start_game_websocket(port:int,
                         map_id : int,
                         power_up_enable : bool,
                         team_left:list[int],
                         team_right:list[int],
                         users_id:list[int],
                         type:int):
    os.system("python3 pong_server/ws_game_server.py " + str(port) + "&")
    await asyncio.sleep(2)
    os.system("echo; echo WS : websocket now running on ws://localhost:" +
              str(port))
    ws = await websockets.connect("ws://localhost:" + str(port))
    msg = {"type":"info",
           "mapId" : map_id,
           "powerUp" : str(power_up_enable).lower(),
           "teamLeft" : team_left,
           "teamRight" : team_right,
           "usersId" : users_id,
           "type" : type}
    str_msg = str(msg).replace("'", '"')
    await ws.send(str_msg)
    await ws.close()
    print("\nWS : all info go to game server", file=sys.stderr)


async def create_new_game(map_id : int,
                          power_up_enable : bool,
                          team_left:list[int],
                          team_right:list[int],
                          users_id:list[int],
                          type:int):
    global number_game_servers_free

    print("\nWS : ALL SERVER :", game_servers, file=sys.stderr)

    for i in range(len(game_servers)):
        if game_servers[i][0] == False:
            game_servers[i][0] = True

            await start_game_websocket(game_servers[i][1],
                                       map_id, power_up_enable,
                                       team_left, team_right, users_id, type)

            return i, game_servers[i][1]

    return None


def end_game(data):
    global game_servers

    # Get port info
    port = data.get("port", None)
    if port == None:
        print("\nWS : MISSING PORT :", data, file=sys.stderr)
        return

    for i in range(len(game_servers)):
        if game_servers[i][1] == port:
            game_servers[i][0] = False
            print("\nWS : SERVER ON PORT", port, "IS NOW FREE", file=sys.stderr)
            print("\nWS : ALL SERVER :", game_servers, file=sys.stderr)

    # Get type info
    type = data.get("type", None)
    if type == None:
        print("\nWS : MISSING TYPE :", data, file=sys.stderr)
        return

    # If the type is quick game, modify money of users
    if type == 0:
        pass
