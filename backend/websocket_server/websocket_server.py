import asyncio
import websockets
import json
import sys
from websocket_server.utils import send_error, set_user_status
from websocket_server.connection import connection_by_token, connection_by_username
from websocket_server.message import recieved_message
from websocket_server.quick_room import join_quick_room, leave_quick_room, \
                                        check_if_can_start_new_game
from websocket_server.game_server_manager import end_game
from websocket_server.game_room import create_game_room, join_game_room, \
                                       quit_game_room, send_game_room_invite, \
                                       game_room_add_bot, game_room_change_team, \
                                       game_room_change_power_up, \
                                       game_room_change_map, game_room_start_game

# Dict to save the actives connections
connected_users = dict()

waitlist = []
game_rooms = dict()
in_game_list = []

def add_user_connected(my_id, websocket):
    lst : list = connected_users.get(my_id, [])
    if len(lst) == 0:
        set_user_status(my_id, 1)
    lst.append(websocket)
    connected_users[my_id] = lst
    print("\nWS : Hello new client " + str(my_id) + " :",
          connected_users, file=sys.stderr)


def remove_user_connected(my_id, websocket, my_game_room_id):
    connected_users.get(my_id, []).remove(websocket)
    print("\nWS : Bye bye client " + str(my_id) + " :",
          connected_users, file=sys.stderr)
    if len(connected_users.get(my_id, [])) == 0:
        set_user_status(my_id, 0)
        leave_quick_room(my_id, waitlist, connected_users)
        if my_game_room_id != None:
            quit_game_room(my_id, connected_users, my_game_room_id, game_rooms)


async def handle_client(websocket : websockets.WebSocketServerProtocol, path):
    my_id = None
    my_game_room_id = None
    print("\nWS : Hello anonymous client", file=sys.stderr)

    try:
        async for data in websocket:
            print("\nWS : DATA RECIEVED :", data, file=sys.stderr)
            data : dict = json.loads(data)

            request_type = data.get("type", None)
            request_cmd = data.get("cmd", None)

            # Check if the common part of the request exist
            if request_type == None or request_cmd == None:
                await send_error(websocket, "Missing type or cmd field in request")
                continue

            # Check connection
            if request_type == "connect":
                ret = None
                if request_cmd == 'by_token':
                    ret = await connection_by_token(websocket, data)
                elif request_cmd == 'by_username':
                    ret = await connection_by_username(websocket, data)
                else:
                    await send_error("Request cmd unkown")

                if ret != None:
                    my_id = ret
                    add_user_connected(my_id, websocket)
                continue

            elif request_type == "gws":
                if request_cmd == 'definitelyNotTheMovie(endGame)':
                    end_game(data, waitlist, in_game_list)
                    await check_if_can_start_new_game(data, connected_users)
                else:
                    await send_error("Request cmd unkown")

            # Check if connected
            if my_id == None:
                await send_error(websocket, "You need to be connected to execute" +
                                 " this request")

            # Message gestion
            if request_type == "message":
                if request_cmd == 'sendMessage':
                    await recieved_message(data, connected_users, websocket, my_id)
                else:
                    await send_error(websocket,
                                     "Request cmd unkown")
                continue

            # Quick game room gestion
            if request_type == "quickRoom":
                if request_cmd == "askForRoom":
                    await join_quick_room(my_id, waitlist, in_game_list,
                                          connected_users)
                elif request_cmd == "quitRoom":
                    await leave_quick_room(my_id, waitlist, connected_users)
                else:
                    await send_error(websocket, "Request cmd unkown")
                continue

            # Game room gestion
            if request_type == "gameRoom":
                if request_cmd == "createRoom":
                    my_game_room_id = await create_game_room(my_id, game_rooms,
                                                             in_game_list,
                                                             connected_users)
                elif request_cmd == "joinRoom":
                    my_game_room_id = await join_game_room(my_id, data,
                                                           game_rooms,
                                                           in_game_list,
                                                           connected_users)
                elif request_cmd == "quitGameRoom":
                    await quit_game_room(my_id, connected_users,
                                         my_game_room_id, game_rooms)
                    my_game_room_id = None
                elif request_cmd == "inviteGameRoom":
                    await send_game_room_invite(my_id, connected_users, data,
                                                my_game_room_id, game_rooms)
                elif request_cmd == "addBot":
                    await game_room_add_bot(my_id, connected_users, data,
                                            my_game_room_id, game_rooms)
                elif request_cmd == "changeTeam":
                    await game_room_change_team(my_id, connected_users, data,
                                                my_game_room_id, game_rooms)
                elif request_cmd == "changePowerUp":
                    await game_room_change_power_up(my_id, connected_users,
                                                    my_game_room_id, game_rooms)
                elif request_cmd == "changeMap":
                    await game_room_change_map(my_id, connected_users, data,
                                               my_game_room_id, game_rooms)
                elif request_cmd == "startGame":
                    ret = await game_room_start_game(my_id, connected_users,
                                                     my_game_room_id, game_rooms,
                                                     in_game_list)
                    # If the creation of the game succeed, remove game id
                    if ret:
                        my_game_room_id = None
                else:
                    await send_error(websocket, "Request cmd unkown")
                continue

            await send_error(websocket, "Request type unkown")

    except Exception as error:
        print("\nWS : CRITICAL ERROR :", error, file=sys.stderr)

    finally:
        # Delete the connection when the client disconnect
        if my_id != None:
            remove_user_connected(my_id, websocket, my_game_room_id)
        else:
            print("\nWS : Bye bye anonymous client", file=sys.stderr)


# Start the websocket server
start_server = websockets.serve(handle_client, "0.0.0.0", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
