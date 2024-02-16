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

print("START GAME SCRIPT (GWS) WITH PARAM :", sys.argv, file=sys.stderr)

# ssl context
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain("/certs/cert.pem")

ssl_context_client = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ssl_context_client.load_verify_locations("/certs/cert.pem")

# Dict to save the actives connections
connected_player = dict()
game = None
can_shutdown = False
# team list will fill by False when create, and fill of True
# when every player are connected
team_left = []
team_right = []
team_left_ready = []
team_right_ready = []
map_id = 0
power_up = False
game_type = 0

websocketPaddleLink = {}

GAME_SERVER_PORT = int(sys.argv[1])

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


async def timeoutConnection():
    global game, team_left_ready, team_right_ready

    print("\nGWS : Start time out connection :", datetime.datetime.now(),
          file=sys.stderr)
    await asyncio.sleep(20)
    print("\nGWS : End time out connection :", datetime.datetime.now(),
          file=sys.stderr)
    print("GWS : Team left ready :", team_left_ready, file=sys.stderr)
    print("GWS : Team right ready :", team_right_ready, file=sys.stderr)

    for readyState in team_left_ready:
        if readyState == False:
            print("GWS : Team left timeout !", file=sys.stderr)
            if game == None:
                asyncio.create_task(game_server_manager())
                await asyncio.sleep(2)
            game.makeTeamWin(1)

    for readyState in team_right_ready:
        if readyState == False:
            print("GWS : Team right timeout !", file=sys.stderr)
            if game == None:
                asyncio.create_task(game_server_manager())
                await asyncio.sleep(2)
            game.makeTeamWin(0)

    print("GWS : NO TIMEOUT", file=sys.stderr)


async def handle_client(websocket : websockets.WebSocketServerProtocol, path):
    global map_id, power_up, team_left_ready, team_right_ready, connected_player, game_type
    # None | (id paddle, id team)
    myid = None
    id_paddle = None
    id_team = None
    id_paddle_with_team = None
    controleDictConvertion = {'up': KEY_UP, 'down': KEY_DOWN, 'powerUp': KEY_POWER_UP, 'launchBall': KEY_LAUNCH_BALL}
    print("\nGWS : Hello anonymous player", path, file=sys.stderr)

    try:
        async for data in websocket:
            # print("\nGWS : DATA RECIEVED :", data, file=sys.stderr)
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
                    id_paddle_with_team = id_paddle + (id_team * TEAM_MAX_PLAYER)
                    websocketPaddleLink[websocket] = id_paddle_with_team
                    if id_team == 0:
                        print("GWS : TEAM LEFT READY", team_left_ready, file=sys.stderr)
                        print("GWS : ID PADDLE", id_paddle, file=sys.stderr)
                        team_left_ready[id_paddle] = True
                    elif id_team == 1:
                        print("GWS : TEAM RIGHT READY", team_right_ready, file=sys.stderr)
                        print("GWS : ID PADDLE", id_paddle, file=sys.stderr)
                        team_right_ready[id_paddle] = True
                    print("\nGWS : TEST IF EVERYONE READY", file=sys.stderr)
                    print("GWS : LTEAM :", team_left_ready, file=sys.stderr)
                    print("GWS : RTEAM :", team_right_ready, file=sys.stderr)
                    if can_start_game():
                        print("GWS : READY TO START : OK", file=sys.stderr)
                        if (game == None):
                            asyncio.create_task(game_server_manager())
                    else:
                        print("GWS : READY TO START : KO", file=sys.stderr)
                continue

            elif request_type == "info":
                print("GWS : RECIVED GAME INFO", file=sys.stderr)
                mapId = data.get("mapId", None)
                powerUp = data.get("powerUp", None)
                teamLeft = data.get("teamLeft", None)
                teamRight = data.get("teamRight", None)
                gameType = data.get("gameType", None)
                if mapId == None or powerUp == None or teamLeft == None or\
                    teamRight == None or gameType == None:
                    print("GWS : MISSING INFO", file=sys.stderr)
                    await send_error(websocket,
                                     "Missing info")
                else:
                    map_id = mapId
                    if powerUp == "true":
                        power_up = True
                    game_type = gameType
                    for id in teamLeft:
                        # If it's an ia, it's ready
                        if id <= -1:
                            team_left_ready.append(True)
                        else:
                            team_left_ready.append(False)
                        team_left.append(id)
                    print("GWS : LTEAM :", team_left_ready, file=sys.stderr)
                    for id in teamRight:
                        # If it's an ia, it's ready
                        if id <= -1:
                            team_right_ready.append(True)
                        else:
                            team_right_ready.append(False)
                        team_right.append(id)
                    print("GWS : RTEAM :", team_right_ready, file=sys.stderr)
                    print("GWS : RECIVED GAME INFO OK", file=sys.stderr)
                    asyncio.create_task(timeoutConnection())
                continue

            # Check if client is connected
            if myid == None:
                await send_error(websocket, "Need to be connected")
                continue

            if request_type == "userInput" and data.get("key", None) != None and data.get("value", None) != None:
                game.messageFromClients.append([CLIENT_MSG_TYPE_USER_EVENT, {"id_paddle":id_paddle_with_team, "id_key":controleDictConvertion[data.get("key", None)],
                                                                             "key_action": data.get("value", None) == "press"}])
            else :
                await send_error(websocket, "Request type unkown")

    except websockets.exceptions.ConnectionClosedOK:
        print("\nGWS : DECONNECTION :", file=sys.stderr)

    except Exception as error:
        print("\nGWS : CRITICAL ERROR :", error, type(error), file=sys.stderr)

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
        # If there is a team, it mean that it's a user
        elif id_team != None:
            # there is no new websocket left for this player, so make if other theam to win
            print("\nGWS : DECONNEXION ?", file=sys.stderr)
            if len(connected_player[myid]) == 0:
                print("GWS : YES", file=sys.stderr)

                # if it's in team left, make team right win
                if id_team == 0:
                    print("GWS : MAKE TEAM RIGHT WIN", file=sys.stderr)
                    game.makeTeamWin(1)
                # if it's in team right, make team left win
                else:
                    print("GWS : MAKE TEAM LEFT WIN", file=sys.stderr)
                    game.makeTeamWin(0)
            else:
                print("GWS : NO", file=sys.stderr)


def can_start_game():
    for state in team_left_ready:
        if not state:
            return False
    for state in team_right_ready:
        if not state:
            return False
    return True


def can_server_shutdown():
    global connected_player
    for lst in connected_player.values():
        if len(lst) > 0:
            return False
    return True


async def sendGlobalMessage(updateObstacles='null', updatePaddles='null',updateBalls='null',deleteBall='null',changeUserPowerUp={},updatePowerUpInGame='null',updateScore='null'):
    global connected_player

    for websockets in connected_player.values():
        for websocket in websockets:
            # print("\nGWS : websocketPaddleLink : ", websocketPaddleLink, file=sys.stderr)
            # print("\nGWS : websockets : ", websockets, file=sys.stderr)
            # print("\nGWS : websocket to find : ", websocket, file=sys.stderr)
            powerUp = changeUserPowerUp.get(websocketPaddleLink[websocket], None)
            if powerUp == None:
                continue
            end_game_msg = {"type" : "serverInfo",
                    "updateObstacles" : updateObstacles,
                    "updatePaddles" : updatePaddles,
                    'updateBalls' : updateBalls,
                    'deleteBall' : deleteBall,
                    'changeUserPowerUp' : powerUp,
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
    changeUserPowerUp={}
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
                updateObstacles.append([obstacle["id"],obstacle["position"], lstPoint])
        if typeContent == SERVER_MSG_TYPE_UPDATE_PADDLES :
            if updatePaddles == 'null' :
                updatePaddles = []
            for paddle in content :
                updatePaddles.append([paddle["position"], paddle["modifierSize"], paddle["id_team"], paddle["id_paddle"], paddle["powerUpInCharge"]])
                changeUserPowerUp[paddle["id_paddle"] + (paddle["id_team"] * TEAM_MAX_PLAYER)] = paddle["powerUp"]
        if typeContent == SERVER_MSG_TYPE_UPDATE_BALLS :
            if updateBalls == 'null' :
                updateBalls = []
            for ball in content :
                updateBalls.append([ball["position"], ball["direction"], ball["radius"], ball["speed"], ball["state"], ball["modifier_state"]])
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
    # print("\nGWS : SEND data to client : ", [updateObstacles, updatePaddles,updateBalls,deleteBall,changeUserPowerUp,updatePowerUpInGame,updateScore], file=sys.stderr)
    # print("\nGWS : SEND updatePowerUpInGame to client : ", updatePowerUpInGame, file=sys.stderr)
    # print("\nGWS : SEND updateBalls to client : ", updateBalls, file=sys.stderr)
    asyncio.create_task(sendGlobalMessage(updateObstacles, updatePaddles,updateBalls,deleteBall,changeUserPowerUp,updatePowerUpInGame,updateScore))

async def countBeforeStart():
    for i in range(6):
        countMsg = {"type" : "startCount",
                    "number": 5 - i,
                    }
        str_msg = str(countMsg)
        str_msg = str_msg.replace("'", '"')

        for websockets in connected_player.values():
            for websocket in websockets:
                await websocket.send(str_msg)
        if (i != 5):
            await asyncio.sleep(1)

async def game_server_manager():
    global game, can_shutdown
    print("\nGWS : START GAME", file=sys.stderr)
    game = GameServer(power_up, team_left, team_right, map_id);
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
    str_msg = str(start_game_msg)
    str_msg = str_msg.replace("'", '"')

    for websockets in connected_player.values():
        for websocket in websockets:
            await websocket.send(str_msg)
    await countBeforeStart()

    while game.runMainLoop : #and (len(connected_player.values()) > 1)
        # print("\nGWS : GAME STEP", file=sys.stderr)
        game.step()
        parsingGlobalMessage()
        await asyncio.sleep(0.01)
    print("\nGWS : END GAME (not the movie)", file=sys.stderr)

    end_game_msg = {"type" : "endGame",
                    "leftTeamScore" : game.teamLeft.score,
                    "rightTeamScore" : game.teamRight.score}
    str_msg = str(end_game_msg)
    str_msg = str_msg.replace("'", '"')

    for websockets in connected_player.values():
        for websocket in websockets:
            await websocket.send(str_msg)

    can_shutdown = True

    print("\nGWS : CHECKIF SERVER CAN SHUTDOWN", file=sys.stderr)
    if can_server_shutdown():
        print("\nGWS : SERVER TRY TO SHUTDOWN", file=sys.stderr)
        os.kill(os.getpid(), signal.SIGTERM)


async def start_server():
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

    async with websockets.serve(handle_client, "0.0.0.0", GAME_SERVER_PORT,
                                ssl=ssl_context):
        await stop
    print("\nGWS : SERVER PORT CLOSE", file=sys.stderr)

    ws = await websockets.connect("wss://localhost:8765", ssl=ssl_context_client)
    msg = {"type":"gws",
            "cmd" : "definitelyNotTheMovie(endGame)",
            "port" : GAME_SERVER_PORT,
            "teamLeft" : team_left,
            "teamRight" : team_right,
            "gameType" : game_type,
            "stats" : game.getFinalStat()}
    str_msg = str(msg).replace("'", '"')
    await ws.send(str_msg)
    await ws.close()
    print("\nGWS : SERVER SHUTDOWN", file=sys.stderr)

print("START GAME WEBSOCKET (GWS) WITH PARAM :", sys.argv, file=sys.stderr)
asyncio.run(start_server())
