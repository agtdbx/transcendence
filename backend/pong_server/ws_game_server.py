import asyncio
import websockets
import json
import sys
import time
from server_code.game_server import GameServer


# Dict to save the actives connections
connected_player = dict()
game = None
game_server_run = True
# team list will fill by False when create, and fill of True when every player are
# connected
team_left = []
team_right = []
map_id = 0
power_up = False


async def send_error(websocket, error_explaination):
    error = {"type" : "error", "error" : error_explaination}
    str_error = str(error)
    str_error = str_error.replace("'", '"')
    await websocket.send(str_error)


def add_user_connected(myid, websocket):
    lst : list = connected_player.get(myid, [])
    lst.append(websocket)
    connected_player[myid] = lst
    print("\nGWS : Hello new player " + str(myid) + " :",
          connected_player, file=sys.stderr)


def remove_user_connected(myid, websocket):
    connected_player.get(myid, []).remove(websocket)
    print("\nGWS : Bye bye player " + str(myid) + " :",
          connected_player, file=sys.stderr)


async def handle_client(websocket : websockets.WebSocketServerProtocol, path):
    global map_id, power_up, team_left, team_right
    # None | (id paddle, id team)
    myid = None
    print("\nGWS : Hello anonymous player", path, file=sys.stderr)

    try:
        async for data in websocket:
            print("\nGWS : DATA RECIEVED :", data, file=sys.stderr)
            data : dict = json.loads(data)
            print("JSON parse OK :", data, file=sys.stderr)

            request_type = data.get("type", None)

            # Check if the common part of the request exist
            if request_type == None:
                await send_error(websocket, "Missing type field in request")
                print("GWS : Missing type field in request :", data,
                      file=sys.stderr)
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
                     await send_error(websocket,
                                     "idPaddle and idTeam must be integer")
                else:
                    myid = (id_paddle, id_team)
                    add_user_connected(myid, connected_player)
                continue

            elif request_type == "info":
                print("\nGWS : DATA RECIEVED ON GAME SERVER :", data,
                        file=sys.stderr)
                mapId = data.get("mapId", None)
                powerUp = data.get("powerUp", None)
                teamLeft = data.get("teamLeft", None)
                teamRight = data.get("teamRight", None)
                if mapId == None or powerUp == None or teamLeft == None or\
                    teamRight == None:
                    await send_error(websocket,
                                     "Missing info")
                else:
                    map_id = mapId
                    power_up = powerUp
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

            await send_error(websocket, "Request type unkown")

    except Exception as error:
        print("\nGWS : CRITICAL ERROR :", error, file=sys.stderr)

    finally:
        # Delete the connection when the client disconnect
        if myid != None:
            remove_user_connected(myid, websocket)
        else:
            print("\nGWS : Bye bye anonymous player", path, file=sys.stderr)
        #if len(connected_player) == 0:
        #    print("\nGWS : No more connection, quitting", file=sys.stderr)
        #    exit()


print("START GAME WEBSOCKET (GWS)", file=sys.stderr)
print("PARAM :", sys.argv, file=sys.stderr)
start_server = websockets.serve(handle_client, "0.0.0.0", int(sys.argv[1]))

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()


# async def game_server_manager(team_left, team_right):
#     global game_server_run
#     # global game
#     number_of_player = len(team_left) + len(team_right)

#     start_time = time.time()

#     while len(connected_player) < number_of_player:
#         print("Wait all player connected", file=sys.stderr)
#         if time.time() - start_time > 60:
#             print("Wait all player TIME OUT", file=sys.stderr)
#             return
#         time.sleep(5)
#     print("START GAME", file=sys.stderr)
#     game.step()
#     time.sleep(15)
#     print("END GAME", file=sys.stderr)

#     end_game_msg = {"type" : "endGame",
#                     "leftTeamScore" : 0,
#                     "rightTeamScore" : 0}
#     str_msg = str(end_game_msg)
#     str_msg = str_msg.replace("'", '"')

#     for _, websockets in connected_player.items():
#         for websocket in websockets:
#             await websocket.send(str_msg)

#     game_server_run = False


# def start_game_server(port:int,
#                       map_id:int,
#                       power_up_enable:bool,
#                       team_left:list[int],
#                       team_right:list[int]):
#     global game, game_server_run
#     # Start the websocket server
#     game = GameServer(power_up_enable, team_left, team_right, map_id)
#     game_server_run = True

#     # asyncio.create_task(game_server_manager(team_left, team_right))

#     start_server = websockets.serve(handle_client, "0.0.0.0", port)

#     asyncio.get_event_loop().run_until_complete(start_server)
#     asyncio.get_event_loop().run_forever()


# async def start_game_thread(port:int,
#                             map_id:int,
#                             power_up_enable:bool,
#                             team_left:list[int],
#                             team_right:list[int],
#                             server_state:list[bool, int]):
#     p = Process(target=start_game_server, args=(port, map_id, power_up_enable, team_left, team_right))
#     p.start()
#     p.join()
#     server_state[0] = False
