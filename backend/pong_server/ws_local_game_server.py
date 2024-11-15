import asyncio
import websockets
import json
import ssl
import sys
import os
import datetime
import signal
from server_code.game_server import GameServer
from define import *

print("START LOCAL GAME SCRIPT (LGWS) WITH PARAM :", sys.argv, file=sys.stderr)

# ssl context
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain("/certs/cert.pem")

ssl_context_client = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ssl_context_client.load_verify_locations("/certs/cert.pem")

# Dict to save the actives connections
connected_player = []
game = None
can_shutdown = False
# team list will fill by False when create, and fill of True
# when every player are connected
team_left = []
team_right = []
map_id = 0
power_up = False
game_type = 0
my_id = None

GAME_SERVER_PORT = int(sys.argv[1])

async def send_error(websocket, error_explaination):
    error = {"type" : "error", "error" : error_explaination}
    str_error = str(error)
    str_error = str_error.replace("'", '"')
    await websocket.send(str_error)


def add_user_connected(websocket):
    global connected_player
    connected_player.append(websocket)
    print("\nLGWS : Hello new player :", connected_player, file=sys.stderr)


def remove_user_connected(websocket):
    global connected_player
    connected_player.remove(websocket)
    print("\nLGWS : Bye bye player :",
          connected_player, file=sys.stderr)


async def timeoutConnection():
    global game

    print("\nLGWS : Start time out connection :", datetime.datetime.now(),
          file=sys.stderr)
    await asyncio.sleep(20)
    print("\nLGWS : End time out connection :", datetime.datetime.now(),
          file=sys.stderr)

    if len(connected_player) == 0:
        print("LGWS : Connection timeout !", file=sys.stderr)
        if game == None:
            asyncio.create_task(game_server_manager())
            await asyncio.sleep(2)
        game.runMainLoop = False
    else:
        print("LGWS : NO TIMEOUT", file=sys.stderr)


async def handle_client(websocket : websockets.WebSocketServerProtocol):
    global map_id, power_up, connected_player, game_type, my_id
    # None | (id paddle, id team)
    connected = False
    controleDictConvertion = {'up': KEY_UP, 'down': KEY_DOWN,
                              'powerUp': KEY_POWER_UP, 'launchBall': KEY_LAUNCH_BALL}
    print("\nLGWS : Hello anonymous player", file=sys.stderr)

    try:
        async for data in websocket:
            # print("\nLGWS : DATA RECIEVED :", data, file=sys.stderr)
            data : dict = json.loads(data)

            request_type = data.get("type", None)

            # Check if the common part of the request exist
            if request_type == None:
                await send_error(websocket, "Missing type field in request")
                continue

            if request_type == "userIdentification":
                add_user_connected(websocket)
                print("LGWS : READY TO START : ", end="", file=sys.stderr)
                if (game == None):
                    print("OK", file=sys.stderr)
                    asyncio.create_task(game_server_manager())
                else:
                    print("KO", file=sys.stderr)
                connected = True
                continue

            elif request_type == "info":
                print("LGWS : RECIVED GAME INFO", file=sys.stderr)
                mapId = data.get("mapId", None)
                powerUp = data.get("powerUp", None)
                teamLeft = data.get("teamLeft", None)
                teamRight = data.get("teamRight", None)
                gameType = data.get("gameType", None)
                my_id = data.get("my_id", None)
                if mapId == None or powerUp == None or teamLeft == None or\
                    teamRight == None or gameType == None:
                    print("LGWS : MISSING INFO", file=sys.stderr)
                    await send_error(websocket,
                                     "Missing info")
                else:
                    map_id = mapId
                    if powerUp == "true":
                        power_up = True
                    game_type = gameType
                    for id in teamLeft:
                        team_left.append(id)
                    for id in teamRight:
                        team_right.append(id)
                    print("LGWS : RECIVED GAME INFO OK", file=sys.stderr)
                    asyncio.create_task(timeoutConnection())
                continue

            # Check if client is connected
            if connected == False:
                await send_error(websocket, "Need to be connected")
                continue

            if request_type == "userInput":
                key = data.get("key", None)
                value = data.get("value", None)
                id_paddle = data.get("idPaddle", None)
                id_team = data.get("idTeam", None)
                if key == None or value == None or id_paddle == None or \
                    id_team == None:
                    await send_error(websocket, "Missing field")
                    continue
                try:
                    id_paddle = int(id_paddle)
                    id_team = int(id_team)
                except:
                    id_paddle = None
                    id_team = None
                    await send_error(websocket,
                                     "idPaddle and idTeam must be integer")
                    continue
                id_paddle_with_team = id_paddle + (id_team * TEAM_MAX_PLAYER)
                game.messageFromClients.append([CLIENT_MSG_TYPE_USER_EVENT,
                                            {"id_paddle" : id_paddle_with_team,
                                             "id_key" : controleDictConvertion[key],
                                             "key_action" : value == "press"}])
            else :
                await send_error(websocket, "Request type unkown")

    except websockets.exceptions.ConnectionClosedOK:
        print("\nLGWS : DECONNECTION :", file=sys.stderr)

    except Exception as error:
        print("\nLGWS : CRITICAL ERROR :", error, type(error), file=sys.stderr)

    finally:
        # Delete the connection when the client disconnect
        if connected:
            remove_user_connected(websocket)
        else:
            print("\nLGWS : Bye bye anonymous player", file=sys.stderr)

        if can_shutdown:
            print("\nLGWS : CHECKIF SERVER CAN SHUTDOWN", file=sys.stderr)
            if len(connected_player) == 0:
                print("\nLGWS : SERVER TRY TO SHUTDOWN", file=sys.stderr)
                os.kill(os.getpid(), signal.SIGTERM)
        # If it's a user
        elif connected:
            # there is no new websocket left for this player
            # so make if other theam to win
            print("\nLGWS : DECONNEXION ?", file=sys.stderr)
            if len(connected_player) == 0:
                print("LGWS : YES", file=sys.stderr)
                game.runMainLoop = False
            else:
                print("LGWS : NO", file=sys.stderr)


async def sendGlobalMessage(updateObstacles='null', updatePaddles='null',
                            updateBalls='null',deleteBall='null',
                            updatePowerUpInGame='null', updateScore='null'):
    global connected_player

    for websocket in connected_player:
        # print("\nLGWS : websockets : ", websockets, file=sys.stderr)
        # print("\nLGWS : websocket to find : ", websocket, file=sys.stderr)
        end_game_msg = {"type" : "serverInfo",
                "updateObstacles" : updateObstacles,
                "updatePaddles" : updatePaddles,
                'updateBalls' : updateBalls,
                'deleteBall' : deleteBall,
                'updatePowerUpInGame' : updatePowerUpInGame,
                'updateScore' : updateScore}
        str_msg = str(end_game_msg)
        str_msg = str_msg.replace("'", '"')
        str_msg = str_msg.replace("False", 'false')
        str_msg = str_msg.replace("True", 'true')
        await websocket.send(str_msg)


def parsingGlobalMessage():
    updateObstacles='null'
    updatePaddles='null'
    updateBalls='null'
    deleteBall='null'
    updatePowerUpInGame='null'
    updateScore='null'

    for changement in game.messageForClients :
        typeContent = changement[0]
        content = changement[1]
        if typeContent == SERVER_MSG_TYPE_UPDATE_OBSTACLE :
            if updateObstacles == 'null' :
                updateObstacles = []
            for obstacle in content :
                lstPoint = []
                for point in obstacle["points"]:
                    lstPoint.append([point[0], point[1]])
                updateObstacles.append([obstacle["id"],obstacle["position"],
                                        lstPoint])
        if typeContent == SERVER_MSG_TYPE_UPDATE_PADDLES :
            if updatePaddles == 'null' :
                updatePaddles = []
            for paddle in content :
                updatePaddles.append([paddle["position"], paddle["modifierSize"],
                                      paddle["id_team"], paddle["id_paddle"],
                                      paddle["powerUpInCharge"], paddle["powerUp"]])
        if typeContent == SERVER_MSG_TYPE_UPDATE_BALLS :
            if updateBalls == 'null' :
                updateBalls = []
            for ball in content :
                updateBalls.append([ball["position"], ball["direction"],
                                    ball["radius"], ball["speed"], ball["state"],
                                    ball["modifier_state"]])
        if typeContent == SERVER_MSG_TYPE_DELETE_BALLS :
            if deleteBall == 'null' :
                deleteBall = []
            deleteBall += content.copy()
        if typeContent == SERVER_MSG_TYPE_UPDATE_POWER_UP :
            if updatePowerUpInGame == 'null' :
                updatePowerUpInGame = []
            updatePowerUpInGame.append(content["position"])
            updatePowerUpInGame.append(content["state"])
        if typeContent == SERVER_MSG_TYPE_SCORE_UPDATE :
            if updateScore == 'null' :
                updateScore = []
            updateScore.append(content['leftTeam'])
            updateScore.append(content['rightTeam'])
    asyncio.create_task(sendGlobalMessage(updateObstacles, updatePaddles,
                                          updateBalls, deleteBall,
                                          updatePowerUpInGame, updateScore))


async def countBeforeStart():
    print("\nLGWS : START TIMER", file=sys.stderr)
    for i in range(6):
        print("\nLGWS : START IN", 5 - i, file=sys.stderr)
        countMsg = {"type" : "startCount",
                    "number": 5 - i,
                    }
        str_msg = str(countMsg)
        str_msg = str_msg.replace("'", '"')

        for websocket in connected_player:
            await websocket.send(str_msg)
        if (i != 5):
            await asyncio.sleep(1)


async def game_server_manager():
    global game, can_shutdown
    print("\nLGWS : START GAME", file=sys.stderr)
    game = GameServer(power_up, team_left, team_right, map_id)
    lstObstacle = []
    for wall in game.walls :
        lstObstacle.append(wall.hitbox.getPoints())

    await asyncio.sleep(0.3)
    start_game_msg = {"type" : "startInfo",
                    "obstacles": lstObstacle ,
                    'powerUp' : str(power_up).lower(),
                    'nbPlayerTeamLeft' : len(team_left),
                    'nbPlayerTeamRight' : len(team_right)
                    }
    str_msg = str(start_game_msg).replace("'", '"')

    for websocket in connected_player:
        await websocket.send(str_msg)
    await countBeforeStart()

    print("\nLGWS : GAME STARTED !!!", file=sys.stderr)
    while game.runMainLoop:
        game.step()
        parsingGlobalMessage()
        await asyncio.sleep(0.01)
    print("\nLGWS : END GAME (not the movie)", file=sys.stderr)

    end_game_msg = {"type" : "endGame",
                    "leftTeamScore" : game.teamLeft.score,
                    "rightTeamScore" : game.teamRight.score}
    str_msg = str(end_game_msg)
    str_msg = str_msg.replace("'", '"')

    for websocket in connected_player:
        await websocket.send(str_msg)

    can_shutdown = True

    print("\nLGWS : CHECKIF SERVER CAN SHUTDOWN", file=sys.stderr)
    if len(connected_player) == 0:
        print("\nLGWS : SERVER TRY TO SHUTDOWN", file=sys.stderr)
        os.kill(os.getpid(), signal.SIGTERM)


async def start_server():
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

    async with websockets.serve(handle_client, "0.0.0.0", GAME_SERVER_PORT,
                                ssl=ssl_context):
        await stop
    print("\nLGWS : SERVER PORT CLOSE", file=sys.stderr)

    ws = await websockets.connect("wss://localhost:8765", ssl=ssl_context_client)
    if my_id == None:
        msg = {"type":"gws",
                "cmd" : "definitelyNotTheMovie(endGame)",
                "port" : GAME_SERVER_PORT,
                "teamLeft" : team_left,
                "teamRight" : team_right,
                "gameType" : game_type,
                "stats" : game.getFinalStat()}
    else:
        msg = {"type":"gws",
                "cmd" : "definitelyNotTheMovie(endGame)",
                "port" : GAME_SERVER_PORT,
                "teamLeft" : team_left,
                "teamRight" : team_right,
                "gameType" : game_type,
                "my_id" : my_id,
                "stats" : game.getFinalStat()}
    str_msg = str(msg).replace("'", '"')
    await ws.send(str_msg)
    await ws.close()
    print("\nLGWS : SERVER SHUTDOWN", file=sys.stderr)

print("START GAME WEBSOCKET (LGWS) WITH PARAM :", sys.argv, file=sys.stderr)
asyncio.run(start_server())
