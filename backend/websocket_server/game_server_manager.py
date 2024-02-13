import os
import asyncio
import sys
import websockets
from websocket_server.utils import set_user_status, get_user_by_id
# from pong_server.ws_game_server import start_game_thread

# List of game server
# List : [server running, port] ; if thread is False, the server is unused
game_servers = [
    [False, 8766],
    [False, 8767],
    [False, 8768],
    [False, 8769],
    [False, 8770]
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
           "type" : type}
    str_msg = str(msg).replace("'", '"')
    await ws.send(str_msg)
    await ws.close()
    print("\nWS : all info go to game server", file=sys.stderr)


async def create_new_game(in_game_list : list,
                          map_id : int,
                          power_up_enable : bool,
                          team_left:list[int],
                          team_right:list[int],
                          type:int):
    print("\nWS : ALL SERVER :", game_servers, file=sys.stderr)

    for i in range(len(game_servers)):
        if game_servers[i][0] == False:
            game_servers[i][0] = True

            await start_game_websocket(game_servers[i][1],
                                       map_id, power_up_enable,
                                       team_left, team_right, type)

            for id in team_left:
                if id != -1:
                    in_game_list.append(id)
                    set_user_status(id, 2)
            for id in team_right:
                if id != -1:
                    in_game_list.append(id)
                    set_user_status(id, 2)

            return i, game_servers[i][1]

    return None


async def end_game(data:dict,
                   in_game_list: list) -> bool:
    global game_servers

    # Get port info
    port = data.get("port", None)
    if port == None:
        print("\nWS : MISSING PORT :", data, file=sys.stderr)
        return None

    for i in range(len(game_servers)):
        if game_servers[i][1] == port:
            game_servers[i][0] = False
            print("\nWS : SERVER ON PORT", port, "IS NOW FREE", file=sys.stderr)
            print("\nWS : ALL SERVER :", game_servers, file=sys.stderr)

    # Get users fielfs
    team_left = data.get("teamLeft", None)
    if team_left == None:
        print("\nWS : Missing info team_left was in game :", data,
              file=sys.stderr)

     # Get users fielfs
    team_right = data.get("teamRight", None)
    if team_right == None:
        print("\nWS : Missing info team_left was in game :", data,
              file=sys.stderr)

    # Set status of users and remove them from in game list
    for id in team_left:
        if id != -1:
            set_user_status(id, 1)
            if id in in_game_list:
                in_game_list.remove(id)

    for id in team_right:
        if id != -1:
            set_user_status(id, 1)
            if id in in_game_list:
                in_game_list.remove(id)

    # Get stats info
    stats = data.get("stats", None)
    if stats == None:
        print("\nWS : MISSING STATS :", data, file=sys.stderr)
        return None

    # GAME STATS
    game_stats = stats[0]

    # TEAM LEFT STATS
    left_team_stats = stats[1]

    # TEAM RIGHT STATS
    right_team_stats = stats[2]

    # BALLS STATS
    balls_stats = stats[3]

    # Get type info
    type = data.get("type", None)
    if type == None:
        print("\nWS : MISSING TYPE :", data, file=sys.stderr)
        return None

    # If the type is quick game, modify money of users
    if type == 0:
        # Get winner and loser
        if game_stats[0] > game_stats[1]:
            user_winner = get_user_by_id(left_team_stats[0][0])
            user_loser = get_user_by_id(right_team_stats[0][0])
        else:
            user_winner = get_user_by_id(right_team_stats[0][0])
            user_loser = get_user_by_id(left_team_stats[0][0])

        print("\nWS : Winner :", user_winner.username, "-", user_winner.money,
              file=sys.stderr)
        print("WS : Loser :", user_loser.username, "-", user_loser.money,
              file=sys.stderr)

        # Update money
        diff = user_winner.money - user_loser.money
        if diff >= 5:
            print("\nWS : +1 -1:", data, file=sys.stderr)
            user_winner.money += 1
            user_loser.money -= 1
        elif diff <= -5:
            print("\nWS : +4 -3:", data, file=sys.stderr)
            user_winner += 4
            user_loser -= 3
        else:
            print("\nWS : +2 -1:", data, file=sys.stderr)
            user_winner += 2
            user_loser -= 1

        if user_loser.money < 0:
            user_loser.money = 0

        user_winner.save()
        user_loser.save()

    winner = None

    # If the type is tournament
    if type == 2:
        if game_stats[0] > game_stats[1]:
            winner = left_team_stats[0][0]
        else:
            winner = right_team_stats[0][0]

    # PUT MATCH IN DB
    # PUT USER MATCH IN DB

    return winner
