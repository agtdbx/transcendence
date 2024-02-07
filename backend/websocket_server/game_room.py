import sys
from websocket_server.utils import send_error, get_user_by_id, set_user_status
from websocket_server.quick_room import create_game_start_message
from websocket_server.game_server_manager import create_new_game, \
                                                 is_game_server_free

#game_rooms
# id : {'creator':<id>,
#       'map_id':<int>,
#       'power_up':<bool>,
#       'team_left':list[<id>],
#       'team_right':list[<id>]}
# If you add an ia, the id will be -1

MAX_PLAYER_PER_TEAM = 2
NUMBER_OF_MAP = 5
IA_ID = -1


async def send_msg_to_id(my_id:int,
                         connected_users:dict,
                         msg:str):
    for websocket in connected_users.get(my_id, []):
        try:
            await websocket.send(msg)
        except:
            pass


async def send_error_to_id(my_id:int,
                           connected_users:dict,
                           error:str):
    for websocket in connected_users.get(my_id, []):
        try:
            await send_error(websocket, error)
        except:
            pass


def create_game_room_status_message(type, game_room:dict):
    msg = {'type' : type,
           'powerUpActivate' : str(game_room['power_up']).lower(),
           'mapId' : game_room['map_id'],
           'teamLeft' : game_room['team_left'],
           'teamRight' :game_room['team_right']}

    str_msg = str(msg).replace("'", '"')
    return str_msg


async def update_message(game_room:dict, connected_users:dict):
    str_msg = create_game_room_status_message("updateRoomInfo", game_room)
    for id in game_room["team_left"]:
        await send_msg_to_id(id, connected_users, str_msg)
    for id in game_room["team_right"]:
        await send_msg_to_id(id, connected_users, str_msg)


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
    room['team_left'].append(my_id)

    game_rooms[room_id] = room

    str_msg = create_game_room_status_message("createRoomInfo", room)

    await send_msg_to_id(my_id, connected_users, str_msg)

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

    # Get game room id from request
    room_id = data.get("gameRoomId", None)
    if room_id == None:
        print("\nWS : User", my_id, "missing room id", file=sys.stderr)
        await send_error_to_id(my_id, connected_users, "Missing room id")
        return None

    # Cast game room in integer
    try:
        room_id = int(room_id)
    except:
        print("\nWS : User", my_id, "room id must be an integer", file=sys.stderr)
        await send_error_to_id(my_id, connected_users,
                               "Room id must be an integer")
        return None

    # Get the room
    game_room = game_rooms.get(room_id, None)
    if game_room == None:
        print("\nWS : User", my_id, "room doesn't exist", file=sys.stderr)
        await send_error_to_id(my_id, connected_users, "Room doesn t exist")
        return None

    # If team right isn't full, put it the new player
    if len(game_room['team_right']) < MAX_PLAYER_PER_TEAM:
        game_room['team_right'].append(my_id)
        str_msg = create_game_room_status_message("joinRoomInfo", game_room)
        await send_msg_to_id(my_id, connected_users, str_msg)
        print("\nWS : User", my_id, "join room", room_id, file=sys.stderr)
        await update_message(game_room, connected_users)
        return room_id
    # If it full, check if there is an ia
    elif IA_ID in game_room['team_right']:
        # If there is an ia, replace the ia by the player
        index = game_room['team_right'].index(IA_ID)
        game_room['team_right'][index] = my_id
        str_msg = create_game_room_status_message("joinRoomInfo", game_room)
        await send_msg_to_id(my_id, connected_users, str_msg)
        print("\nWS : User", my_id, "join room", room_id, file=sys.stderr)
        await update_message(game_room, connected_users)
        return room_id

    # If team left isn't full, put it the new player
    if len(game_room['team_left']) < MAX_PLAYER_PER_TEAM:
        game_room['team_left'].append(my_id)
        str_msg = create_game_room_status_message("joinRoomInfo", game_room)
        await send_msg_to_id(my_id, connected_users, str_msg)
        print("\nWS : User", my_id, "join room", room_id, file=sys.stderr)
        await update_message(game_room, connected_users)
        return room_id
    # If it full, check if there is an ia
    elif IA_ID in game_room['team_left']:
        index = game_room['team_left'].index(IA_ID)
        game_room['team_left'][index] = my_id
        str_msg = create_game_room_status_message("joinRoomInfo", game_room)
        await send_msg_to_id(my_id, connected_users, str_msg)
        print("\nWS : User", my_id, "join room", room_id, file=sys.stderr)
        await update_message(game_room, connected_users)
        return room_id

    # Game room is full
    print("\nWS : User", my_id, "all teams are full", file=sys.stderr)
    await send_error_to_id(my_id, connected_users, "All teams are full")
    return None


async def quit_game_room(my_id:int,
                         connected_users:dict,
                         game_room_id:int,
                         game_rooms:dict):
    # Check if the room exist
    game_room = game_rooms.get(game_room_id, None)
    if game_room == None:
        print("\nWS : User", my_id, "room doesn't exist", file=sys.stderr)
        await send_error_to_id(my_id, connected_users, "Room doesn t exist")
        return

    # If the user is the creator, quick everyone from the room
    if game_room['creator'] == my_id:
        str_msg = str({"type":"quitGameRoom"}).replace("'", '"')
        await send_msg_to_id(my_id, connected_users, str_msg)
        str_msg = str({"type":"quickFromGameRoom"}).replace("'", '"')
        for user_id in game_room['team_left']:
            if user_id != my_id:
                await send_msg_to_id(user_id, connected_users, str_msg)
        for user_id in game_room['team_right']:
            if user_id != my_id:
                await send_msg_to_id(user_id, connected_users, str_msg)
        game_rooms.pop(game_room_id)
        print("\nWS : User", my_id, "create quit and destroy game room",
              file=sys.stderr)
        return

    # Check if user is in team left
    if my_id in game_room['team_left']:
        print("\nWS : Remove user", my_id, "from left team", file=sys.stderr)
        game_room['team_left'].remove(my_id)
    # Check if user is in team right
    elif my_id in game_room['team_right']:
        print("\nWS : Remove user", my_id, "from right team", file=sys.stderr)
        game_room['team_right'].remove(my_id)
    # The user isn't in the room
    else:
        print("\nWS : User", my_id, "is not in the room", file=sys.stderr)
        await send_error_to_id(my_id, connected_users, "User not in room")
        return

    # Send to player in room that user leave it
    print("\nWS : User", my_id, "quit game room", file=sys.stderr)
    str_msg = str({"type":"quitGameRoom"}).replace("'", '"')
    await send_msg_to_id(my_id, connected_users, str_msg)

    # Update message
    await update_message(game_room, connected_users)


async def send_game_room_invite(my_id:int,
                                connected_users:dict,
                                data:dict,
                                game_room_id:int,
                                game_rooms:dict):
    # Check if the room exist
    game_room:dict = game_rooms.get(game_room_id, None)
    if game_room == None:
        print("\nWS : User", my_id, "room doesn't exist", file=sys.stderr)
        await send_error_to_id(my_id, connected_users, "Room doesn t exist")
        return

    # Check if user if the room creator
    if my_id != game_room["creator"]:
        print("\nWS : User", my_id, "isn't the room creator", file=sys.stderr)
        await send_error_to_id(my_id, connected_users, "Must be room s creator")
        return

    # Get the target info
    target = data.get("targetId", None)
    if target == None:
        print("\nWS : User", my_id, "missing target field", file=sys.stderr)
        await send_error_to_id(my_id, connected_users, "Missing target field")
        return

    try:
        target = int(target)
    except:
        print("\nWS : User", my_id, "Target must be an integer", file=sys.stderr)
        await send_error_to_id(my_id, connected_users, "Target must be an integer")
        return

    # Check if the target is already in the room
    if target in game_room['team_left'] or target in game_room['team_right']:
        print("\nWS : User", my_id, "Target already in room", file=sys.stderr)
        await send_error_to_id(my_id, connected_users, "Target already in room")
        return

    # If user can join
    if len(game_room['team_right']) < MAX_PLAYER_PER_TEAM or \
        IA_ID in game_room['team_right'] or \
        len(game_room['team_left']) < MAX_PLAYER_PER_TEAM or \
        IA_ID in game_room['team_left']:
        # Send invite
        user = get_user_by_id(my_id)
        if user == None:
            print("\nWS : User", my_id, "not foud", file=sys.stderr)
            await send_error_to_id(my_id, connected_users, "User not found")

        str_msg = str({"type" : "invite",
                       "username" : user.username,
                       "pp" : str(user.profilPicture),
                       "roomId" : game_room_id}).replace("'", '"')
        await send_msg_to_id(target, connected_users, str_msg)
        return

    # User can't join
    print("\nWS : User", my_id, "room is full", file=sys.stderr)
    await send_error_to_id(my_id, connected_users, "Room is full")


async def game_room_add_bot(my_id:int,
                            connected_users:dict,
                            data:dict,
                            game_room_id:int,
                            game_rooms:dict):
    # Check if the room exist
    game_room:dict = game_rooms.get(game_room_id, None)
    if game_room == None:
        print("\nWS : User", my_id, "room doesn't exist", file=sys.stderr)
        await send_error_to_id(my_id, connected_users, "Room doesn t exist")
        return

    # Check if user if the room creator
    if my_id != game_room["creator"]:
        print("\nWS : User", my_id, "isn't the room creator", file=sys.stderr)
        await send_error_to_id(my_id, connected_users, "Must be room s creator")
        return

    # Get team field from data
    target_team = data.get("team", None)
    if target_team == None:
        print("\nWS : User", my_id, "missing team field", file=sys.stderr)
        await send_error_to_id(my_id, connected_users, "Missing team field")
        return

    # Join left team
    if target_team == "left":
        # Check if team is full
        if len(game_room["team_left"]) >= MAX_PLAYER_PER_TEAM:
            print("\nWS : User", my_id, "Left team full", file=sys.stderr)
            await send_error_to_id(my_id, connected_users, "Left team full")
            return
        game_room["team_left"].append(IA_ID)

    # Join right team
    elif target_team == "right":
        # Check if team is full
        if len(game_room["team_right"]) >= MAX_PLAYER_PER_TEAM:
            print("\nWS : User", my_id, "Right team full", file=sys.stderr)
            await send_error_to_id(my_id, connected_users, "Right team full")
            return
        game_room["team_right"].append(IA_ID)

    else:
        # Team field is incorrect
        print("\nWS : User", my_id, "team is only left or right", file=sys.stderr)
        await send_error_to_id(my_id, connected_users,
                                "Team is only left or right")

    # Update message
    await update_message(game_room, connected_users)


async def game_room_change_team(my_id:int,
                                connected_users:dict,
                                data:dict,
                                game_room_id:int,
                                game_rooms:dict):
    # Check if the room exist
    game_room:dict = game_rooms.get(game_room_id, None)
    if game_room == None:
        print("\nWS : User", my_id, "room doesn't exist", file=sys.stderr)
        await send_error_to_id(my_id, connected_users, "Room doesn t exist")
        return

    # Get team field from data
    target_team = data.get("team", None)
    if target_team == None:
        print("\nWS : User", my_id, "missing team field", file=sys.stderr)
        await send_error_to_id(my_id, connected_users, "Missing team field")
        return

    if target_team == "left":
        # If user is already in team
        if my_id in game_room["team_left"]:
            print("\nWS : User", my_id, "Already in left team", file=sys.stderr)
            await send_error_to_id(my_id, connected_users, "Already in left team")
            return
        # If team left have enough place
        if len(game_room["team_left"]) < MAX_PLAYER_PER_TEAM:
            game_room["team_right"].remove(my_id)
            game_room["team_left"].append(my_id)
        # If team left have ia to replace
        elif IA_ID in game_room["team_left"]:
            game_room["team_right"].remove(my_id)
            index = game_room["team_left"].index(IA_ID)
            game_room["team_left"][index] = my_id
        # Team left full
        else :
            print("\nWS : User", my_id, "Left team is full", file=sys.stderr)
            await send_error_to_id(my_id, connected_users, "Left team is full")
            return

    elif target_team == "right":
        # If user is already in team
        if my_id in game_room["team_right"]:
            print("\nWS : User", my_id, "Already in right team", file=sys.stderr)
            await send_error_to_id(my_id, connected_users, "Already in right team")
            return
        # If team right have enough place
        if len(game_room["team_right"]) < MAX_PLAYER_PER_TEAM:
            game_room["team_left"].remove(my_id)
            game_room["team_right"].append(my_id)
        # If team right have ia to replace
        elif IA_ID in game_room["team_right"]:
            game_room["team_left"].remove(my_id)
            index = game_room["team_right"].index(IA_ID)
            game_room["team_right"][index] = my_id
        # Team right full
        else :
            print("\nWS : User", my_id, "Right team is full", file=sys.stderr)
            await send_error_to_id(my_id, connected_users, "Right team is full")
            return

    else:
        # Team field is incorrect
        print("\nWS : User", my_id, "team is only left or right", file=sys.stderr)
        await send_error_to_id(my_id, connected_users,
                                "Team is only left or right")

    # Update message
    await update_message(game_room, connected_users)


async def game_room_change_power_up(my_id:int,
                         connected_users:dict,
                         game_room_id:int,
                         game_rooms:dict):
    # Check if the room exist
    game_room:dict = game_rooms.get(game_room_id, None)
    if game_room == None:
        print("\nWS : User", my_id, "room doesn't exist", file=sys.stderr)
        await send_error_to_id(my_id, connected_users, "Room doesn t exist")
        return

    # Check if user if the room creator
    if my_id != game_room["creator"]:
        print("\nWS : User", my_id, "isn't the room creator", file=sys.stderr)
        await send_error_to_id(my_id, connected_users, "Must be room s creator")
        return

    game_room['power_up'] = not game_room['power_up']

    print("\nWS : User", my_id, "change power up to", game_room['power_up'],
          file=sys.stderr)
    # Update message
    await update_message(game_room, connected_users)


async def game_room_change_map(my_id:int,
                         connected_users:dict,
                         data:dict,
                         game_room_id:int,
                         game_rooms:dict):
    # Check if the room exist
    game_room:dict = game_rooms.get(game_room_id, None)
    if game_room == None:
        print("\nWS : User", my_id, "room doesn't exist", file=sys.stderr)
        await send_error_to_id(my_id, connected_users, "Room doesn t exist")
        return

    # Check if user if the room creator
    if my_id != game_room["creator"]:
        print("\nWS : User", my_id, "isn't the room creator", file=sys.stderr)
        await send_error_to_id(my_id, connected_users, "Must be room s creator")
        return

    # Get map id field
    new_map = data.get("mapId", None)
    if new_map == None:
        print("\nWS : User", my_id, "Missing mapId field", file=sys.stderr)
        await send_error_to_id(my_id, connected_users, "Missing mapId field")
        return

    # Cast map id to integer
    try:
        new_map = int(new_map)
    except:
        print("\nWS : User", my_id, "mapId must be an integer", file=sys.stderr)
        await send_error_to_id(my_id, connected_users, "mapId must be an integer")
        return

    if new_map < 0 or new_map >= NUMBER_OF_MAP:
        print("\nWS : User", my_id, "mapId must be beetween 0 and",
              NUMBER_OF_MAP - 1, file=sys.stderr)
        await send_error_to_id(my_id, connected_users,
                               "mapId must be beetween 0 and " +
                               str(NUMBER_OF_MAP - 1))
        return

    game_room["map_id"] = new_map

    print("\nWS : User", my_id, "change map to", new_map, file=sys.stderr)
    # Update message
    await update_message(game_room, connected_users)


async def game_room_start_game(my_id:int,
                         connected_users:dict,
                         game_room_id:int,
                         game_rooms:dict,
                         in_game_list:list):
    # Check if the room exist
    game_room:dict = game_rooms.get(game_room_id, None)
    if game_room == None:
        print("\nWS : User", my_id, "room", game_room_id, "doesn't exist",
              file=sys.stderr)
        await send_error_to_id(my_id, connected_users, "Room doesn t exist")
        return False
    print("\nWS : User", my_id, "room check ok", file=sys.stderr)

    # Check if user if the room creator
    if my_id != game_room["creator"]:
        print("\nWS : User", my_id, "isn't the room creator", file=sys.stderr)
        await send_error_to_id(my_id, connected_users, "Must be room s creator")
        return False
    print("\nWS : User", my_id, "permisson check ok", file=sys.stderr)

    if len(game_room['team_left']) == 0:
        print("\nWS : User", my_id, "Team left empty", file=sys.stderr)
        await send_error_to_id(my_id, connected_users, "Team left empty")
        return False
    print("\nWS : User", my_id, "team left check ok", file=sys.stderr)

    if len(game_room['team_right']) == 0:
        print("\nWS : User", my_id, "Team right empty", file=sys.stderr)
        await send_error_to_id(my_id, connected_users, "Team right empty")
        return False
    print("\nWS : User", my_id, "team right check ok", file=sys.stderr)

    if not is_game_server_free():
        print("\nWS : User", my_id, "No server free", file=sys.stderr)
        await send_error_to_id(my_id, connected_users, "No server free")
        return False
    print("\nWS : User", my_id, "game server free", file=sys.stderr)

    users_id = []
    paddles = []
    # Create left team info for game creation
    team_left = list()
    for i in range(len(game_room["team_left"])):
        id = game_room["team_left"][i]
        if id == IA_ID:
            team_left.append(1)
        else:
            users_id.append(id)
            paddles.append((id, i, 0))
            team_left.append(0)

    # Same for right team
    team_right = list()
    for i in range(len(game_room["team_right"])):
        id = game_room["team_right"][i]
        if id == IA_ID:
            team_right.append(1)
        else:
            users_id.append(id)
            paddles.append((id, i, 1))
            team_right.append(0)

    # team [int, int]
    # int per paddle, 0 for player, 1 for ia
    ret = await create_new_game(game_room["map_id"], game_room["power_up"],
                                team_left, team_right, users_id)

    if ret == None:
        print("\nWS : ERROR : No game server free, put user", my_id, "in waitlist",
              file=sys.stderr)
        return False
    print("\nWS : User", my_id, "game server ok", file=sys.stderr)

    game_rooms.pop(game_room_id)

    for user_id, paddle_id, team_id in paddles:
        set_user_status(user_id, 2)
        in_game_list.append(user_id)
        str_msg = create_game_start_message(ret[1], paddle_id, team_id)
        await send_msg_to_id(user_id, connected_users, str_msg)

    return True
