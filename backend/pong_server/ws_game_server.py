import asyncio
import websockets
import json
import sys
import os
import time
import signal
from server_code.game_server import GameServer


# Dict to save the actives connections
connected_player = dict()
game = None
can_shutdown = False
# team list will fill by False when create, and fill of True
# when every player are connected
team_left = []
team_right = []
map_id = 0
power_up = False
users_id = []

async def send_error(websocket, error_explaination):
    error = {"type" : "error", "error" : error_explaination}
    str_error = str(error)
    str_error = str_error.replace("'", '"')
    await websocket.send(str_error)


def add_user_connected(myid, websocket):
    global connected_player
    lst : list = connected_player.get(myid, [])
    lst.append(websocket)
    connected_player[myid] = lst
    print("\nGWS : Hello new player " + str(myid) + " :",
          connected_player, file=sys.stderr)


def remove_user_connected(myid, websocket):
    global connected_player
    connected_player.get(myid, []).remove(websocket)
    print("\nGWS : Bye bye player " + str(myid) + " :",
          connected_player, file=sys.stderr)


async def handle_client(websocket : websockets.WebSocketServerProtocol, path):
    global map_id, power_up, team_left, team_right, connected_player, users_id
    # None | (id paddle, id team)
    myid = None
    id_paddle = None
    id_team = None
    print("\nGWS : Hello anonymous player", path, file=sys.stderr)

    try:
        async for data in websocket:
            print("\nGWS : DATA RECIEVED :", data, file=sys.stderr)
            data : dict = json.loads(data)

            request_type = data.get("type", None)

            # Check if the common part of the request exist
            if request_type == None:
                await send_error(websocket, "Missing type field in request")
                continue

            if request_type == "userIdentification":
                id_paddle = data.get("idPaddle", None)
                id_team = data.get("idTeam", None)
                if id_paddle == None or id_team == None:
                    await send_error(websocket,
                                     "Missing idPaddle or idTeam")
                    continue
                try:
                    id_paddle = int(id_paddle)
                    id_team = int(id_team)
                except:
                    id_paddle = None
                    id_team = None
                    await send_error(websocket,
                                     "idPaddle and idTeam must be integer")
                else:
                    myid = (id_paddle, id_team)
                    add_user_connected(myid, websocket)
                    if id_team == 0:
                        team_left[id_paddle] = True
                    elif id_team == 1:
                        team_right[id_paddle] = True
                    print("\nGWS : TEST IF EVERYONE READY", file=sys.stderr)
                    print("GWS : LTEAM :", team_left, file=sys.stderr)
                    print("GWS : RTEAM :", team_right, file=sys.stderr)
                    if can_start_game():
                        print("GWS : OK", file=sys.stderr)
                        asyncio.create_task(game_server_manager())
                    else:
                        print("GWS : KO", file=sys.stderr)
                continue

            elif request_type == "info":
                mapId = data.get("mapId", None)
                powerUp = data.get("powerUp", None)
                teamLeft = data.get("teamLeft", None)
                teamRight = data.get("teamRight", None)
                usersId = data.get("usersId", None)
                if mapId == None or powerUp == None or teamLeft == None or\
                    teamRight == None or usersId == None:
                    await send_error(websocket,
                                     "Missing info")
                else:
                    map_id = mapId
                    power_up = powerUp
                    users_id = usersId
                    size = len(teamLeft)
                    team_left = [False] * size
                    for i in range(size):
                        # If it's an ia, it's ready
                        if teamLeft[i] == 1:
                            team_left[i] = True
                    size = len(teamRight)
                    team_right = [False] * size
                    for i in range(size):
                        # If it's an ia, it's ready
                        if teamRight[i] == 1:
                            team_right[i] = True
                continue
            
            # Check if client is connected
            if myid == None:
                await send_error(websocket, "Need to be connected")
                continue

            await send_error(websocket, "Request type unkown")

    except Exception as error:
        print("\nGWS : CRITICAL ERROR :", error, file=sys.stderr)

    finally:
        # Delete the connection when the client disconnect
        if myid != None:
            remove_user_connected(myid, websocket)
        else:
            print("\nGWS : Bye bye anonymous player", path, file=sys.stderr)

        if can_shutdown:
            print("\nGWS : CHECKIF SERVER CAN SHUTDOWN", file=sys.stderr)
            if can_server_shutdown():
                print("\nGWS : SERVER TRY TO SHUTDOWN", file=sys.stderr)
                os.kill(os.getpid(), signal.SIGTERM)


def can_start_game():
    for state in team_left:
        if not state:
            return False
    for state in team_right:
        if not state:
            return False
    return True


def can_server_shutdown():
    global connected_player
    for lst in connected_player.values():
        if len(lst) > 0:
            return False
    return True

async def sendGlobalMessage(updateObstacles='null', updatePaddles='null',updateBalls='null',deleteBall='null',changeUserPowerUp='null',updatePowerUpInGame='null',updateScore='null'):
    end_game_msg = {"type" : "serverInfo",
                    "updateObstacles" : [],
                    "updatePaddles" : [],
                    'updateBalls' : [],
                    'deleteBall' : null,
                    'changeUserPowerUp' : 0,
                    'updatePowerUpInGame' : 0,
                    'updateScore' : 0}
    str_msg = str(end_game_msg)
    str_msg = str_msg.replace("'", '"')

    for websockets in connected_player.values():
        for websocket in websockets:
            await websocket.send(str_msg)

async def game_server_manager():
    global game, can_shutdown
    print("\nGWS : START GAME", file=sys.stderr)
    game = GameServer(power_up, team_left, team_right, map_id);
    lstObstacle = []
    for wall in game.walls :
        lstObstacle.append(wall.hitbox.getPoints())
    
    await asyncio.sleep(3)
    end_game_msg = {"type" : "startInfo",
                    "obstacles": lstObstacle ,
                    'powerUp' : power_up
                    }
    str_msg = str(end_game_msg)
    str_msg = str_msg.replace("'", '"')

    for websockets in connected_player.values():
        for websocket in websockets:
            await websocket.send(str_msg)


    while game.runMainLoop :
        print("\nGWS : GAME STEP", file=sys.stderr)
        game.step()
        await asyncio.sleep(0.1)
    print("\nGWS : END GAME (not the movie)", file=sys.stderr)

    end_game_msg = {"type" : "endGame",
                    "leftTeamScore" : 0,
                    "rightTeamScore" : 0}
    str_msg = str(end_game_msg)
    str_msg = str_msg.replace("'", '"')

    for websockets in connected_player.values():
        for websocket in websockets:
            await websocket.send(str_msg)

    can_shutdown = True


async def start_server():
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

    async with websockets.serve(handle_client, "0.0.0.0", int(sys.argv[1])):
        await stop
    print("\nGWS : SERVER PORT CLOSE", file=sys.stderr)

    ws = await websockets.connect("ws://localhost:8765")
    # TODO : Need to return all statistique of the game !
    msg = {"type":"gws",
            "cmd" : "definitelyNotTheMovie(endGame)",
            "port" : int(sys.argv[1]),
            "usersId" : users_id}
    str_msg = str(msg).replace("'", '"')
    await ws.send(str_msg)
    await ws.close()
    print("\nGWS : SERVER SHUTDOWN", file=sys.stderr)

print("START GAME WEBSOCKET (GWS) WITH PARAM :", sys.argv, file=sys.stderr)
asyncio.run(start_server())
