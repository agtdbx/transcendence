import sys
from websocket_server.utils import send_error
from websocket_server.game_server_manager import create_new_game, \
                                                 is_game_server_free

#game_rooms
# id : {'creator':<id>,
#       'map_id':<int>,
#       'power_up':<bool>,
#       'team_left':list[{'id':<id>, 'state':<int>}],
#       'team_right':list[{'id':<id>, 'state':<int>}]}
# If you add an ia, the id will be -1
# State : 0 -> not ready
#         1 -> ready
#         2 -> waiting the invite reply

MAX_PLAYER_PER_TEAM = 2

async def send_msg_to_id(my_id:int,
                         connected_users:dict,
                         msg:str):
    for websocket in connected_users.get(my_id, []):
        await websocket.send(msg)


async def send_error_to_id(my_id:int,
                           connected_users:dict,
                           error:str):
    for websocket in connected_users.get(my_id, []):
        await send_error(websocket, error)


def create_game_room_status_message(type, game_room:dict):
    msg = {'type' : type,
           'powerUpActivate' : str(game_room['power_up']).lower(),
           'mapId' : game_room['map_id'],
           'teamLeft' : [],
           'teamRight' : []}

    for paddle in game_room['team_left']:
        msg['teamLeft'].append(list(paddle.values()))

    for paddle in game_room['team_right']:
        msg['teamRight'].append(list(paddle.values()))

    str_msg = str(msg).replace("'", '"')
    return str_msg


async def create_game_room(my_id : int,
                          game_rooms : dict,
                          in_game_list: list,
                          connected_users : dict):
    # If the user is already in game, don't create the room
    if my_id in in_game_list:
        print("\nWS : User", my_id, "already in game", file=sys.stderr)
        return None

    room_id = len(game_rooms)

    # create the room
    print("\nWS : User", my_id, "create the game room", room_id, file=sys.stderr)
    room = {'creator' : my_id,
            'map_id' : 0,
            'power_up' : False,
            'team_left' : list(),
            'team_right' : list()
            }
    room['team_left'].append({'id' : my_id, 'state' : 0})

    game_rooms[room_id] = room

    str_msg = create_game_room_status_message("createRoomInfo", room)

    send_msg_to_id(my_id, connected_users, str_msg)

    return room_id


async def join_game_room(my_id:int,
                         data:dict,
                         game_rooms : dict,
                         in_game_list: list,
                         connected_users : dict):
    # If the user is already in game, don't create the room
    if my_id in in_game_list:
        print("\nWS : User", my_id, "already in game", file=sys.stderr)
        return None

    room_id = None

    room_id = data.get("gameRoomId", None)
    if room_id == None:
        print("\nWS : User", my_id, "missing room id", file=sys.stderr)
        await send_error_to_id(my_id, connected_users, "Missing room id")
        return None

    try:
        room_id = int(room_id)

    except:
        print("\nWS : User", my_id, "room id must be an integer", file=sys.stderr)
        await send_error_to_id(my_id, connected_users,
                               "Room id must be an integer")
        return None

    room = game_rooms.get(room_id, None)
    if room == None:
        print("\nWS : User", my_id, "room doesn't exist", file=sys.stderr)
        await send_error_to_id(my_id, connected_users,
                               "Room doesn't exist")
        return None

    if len(room['team_left'] < MAX_PLAYER_PER_TEAM):
        room['team_left'].append({'id' : my_id, 'state' : 0})
        str_msg = create_game_room_status_message("joinRoomInfo", room)
        await send_msg_to_id(my_id, connected_users, str_msg)
        print("\nWS : User", my_id, "join room", room_id, file=sys.stderr)
        return room_id

    if len(room['team_right'] < MAX_PLAYER_PER_TEAM):
        room['team_right'].append({'id' : my_id, 'state' : 0})
        str_msg = create_game_room_status_message("joinRoomInfo", room)
        await send_msg_to_id(my_id, connected_users, str_msg)
        print("\nWS : User", my_id, "join room", room_id, file=sys.stderr)
        return room_id

    print("\nWS : User", my_id, "all teams are full", file=sys.stderr)
    await send_error_to_id(my_id, connected_users, "All teams are full")
    return None


async def quit_game_room(my_id:int,
                         connected_users:dict,
                         game_room_id:int,
                         game_rooms:dict):
    game_room = game_rooms.get(game_room_id, None)
    if game_room == None:
        print("\nWS : User", my_id, "room doesn't exist", file=sys.stderr)
        await send_error_to_id(my_id, connected_users,
                               "Room doesn't exist")
        return

    if game_room['creator'] == my_id:
        str_msg = str({"type":"quitGameRoom"}).replace("'", '"')
        await send_msg_to_id(my_id, connected_users, str_msg)
        str_msg = str({"type":"quickFromGameRoom"}).replace("'", '"')
        for paddle in game_room['team_left']:
            if paddle['id'] != my_id:
                await send_msg_to_id(paddle['id'], connected_users, str_msg)
        for paddle in game_room['team_right']:
            if paddle['id'] != my_id:
                await send_msg_to_id(paddle['id'], connected_users, str_msg)
        game_rooms.pop(game_room_id)
        return

    # Check if user is in team left
    i = None
    team = 'left'
    for j in range(len(game_room['team_left'])):
        paddle = game_room['team_left'][j]
        if paddle['id'] == my_id:
            i = j
            break

    # Check if user is in team right
    if i != None:
        team = 'right'
        for j in range(len(game_room['team_right'])):
            paddle = game_room['team_right'][j]
            if paddle['id'] == my_id:
                i = j
                break

    if i != None:
        if team == 'left':
            print("\nWS : Remove user", my_id, "from left team", file=sys.stderr)
            game_room['team_left'].pop(i)
        else:
            print("\nWS : Remove user", my_id, "from right team", file=sys.stderr)
            game_room['team_right'].pop(i)

        str_msg = str({"type":"quitGameRoom"}).replace("'", '"')
        await send_msg_to_id(my_id, connected_users, str_msg)

        str_msg = create_game_room_status_message("quitGameRoom", game_room)
        for paddle in game_room['team_left']:
            await send_msg_to_id(paddle['id'], connected_users, str_msg)
        for paddle in game_room['team_right']:
            await send_msg_to_id(paddle['id'], connected_users, str_msg)
        return

    print("\nWS : User", my_id, "is not in the room", file=sys.stderr)
    await send_error_to_id(my_id, connected_users, "User not in room")
    return
