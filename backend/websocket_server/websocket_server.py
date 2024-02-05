import asyncio
import websockets
import json
import sys
from websocket_server.utils import send_error, set_user_status
from websocket_server.connection import connection_by_token, connection_by_username
from websocket_server.message import recieved_message
from websocket_server.quick_room import join_quick_room, leave_quick_room, check_if_can_start_new_game
from websocket_server.game_server_manager import end_game

# Dict to save the actives connections
connected_users = dict()

waitlist = []
game_rooms = dict()
in_game_list = []

def add_user_connected(myid, websocket):
    lst : list = connected_users.get(myid, [])
    if len(lst) == 0:
        set_user_status(myid, 1)
    lst.append(websocket)
    connected_users[myid] = lst
    print("\nWS : Hello new client " + str(myid) + " :",
          connected_users, file=sys.stderr)


def remove_user_connected(myid, websocket):
    connected_users.get(myid, []).remove(websocket)
    print("\nWS : Bye bye client " + str(myid) + " :",
          connected_users, file=sys.stderr)
    if len(connected_users.get(myid, [])) == 0:
        set_user_status(myid, 0)
        leave_quick_room(myid, waitlist, connected_users)


async def handle_client(websocket : websockets.WebSocketServerProtocol, path):
    myid = None
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
                    myid = ret
                    add_user_connected(myid, websocket)
                continue

            elif request_type == "gws":
                if request_cmd == 'definitelyNotTheMovie(endGame)':
                    end_game(data, waitlist, in_game_list)
                    await check_if_can_start_new_game(data, connected_users)
                else:
                    await send_error("Request cmd unkown")

            # Check if connected
            if myid == None:
                await send_error(websocket, "You need to be connected to execute" +
                                 " this request")

            # Message gestion
            if request_type == "message":
                if request_cmd == 'sendMessage':
                    await recieved_message(data, connected_users, websocket, myid)
                else:
                    await send_error(websocket,
                                     "Request cmd unkown")
                continue

            # Quick game room gestion
            if request_type == "quickRoom":
                if request_cmd == "askForRoom":
                    await join_quick_room(myid, waitlist, in_game_list,
                                          connected_users)
                elif request_cmd == "quitRoom":
                    await leave_quick_room(myid, waitlist, connected_users)
                else:
                    await send_error(websocket, "Request cmd unkown")
                continue

            await send_error(websocket, "Request type unkown")

    except Exception as error:
        print("\nWS : CRITICAL ERROR :", error, file=sys.stderr)

    finally:
        # Delete the connection when the client disconnect
        if myid != None:
            remove_user_connected(myid, websocket)
        else:
            print("\nWS : Bye bye anonymous client", file=sys.stderr)


# Start the websocket server
start_server = websockets.serve(handle_client, "0.0.0.0", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
