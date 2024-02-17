import sys
from websocket_server.utils import send_error_to_id, send_msg_to_id, \
                                   get_user_by_id, get_map_name_by_id, \
                                   create_game_start_message, \
                                   GAME_TYPE_LOCAL_CUSTOM, \
                                   NUMBER_OF_MAP, IA_ID
from websocket_server.game_server_manager import create_new_local_game, \
                                                 is_game_server_free

#game_room
# id : {'map_id':<int>,
#       'power_up':<bool>,
#       'team_left':list[<id>],
#       'team_right':list[<id>]}
# If you add an ia, the id will be -1

MAX_PLAYER_PER_TEAM = 2


def get_list_user_view(list_user_id):
    list_user_view = []
    for user_id in list_user_id:
        user = get_user_by_id(user_id)
        if user == None:
            continue
        list_user_view.append(["/static/" + user.profilPicture.name, user.username, user.idUser])

    return list_user_view


def create_game_room_status_message(type, game_room:dict):
    msg = {'type' : type,
           'powerUpActivate' : str(game_room['power_up']).lower(),
           'mapId' : game_room['map_id'],
           'mapName' : get_map_name_by_id(game_room['map_id']),
           'teamLeft' : get_list_user_view(game_room['team_left']),
           'teamRight' : get_list_user_view(game_room['team_right'])}

    str_msg = str(msg).replace("'", '"')
    return str_msg


async def create_local_game_room(my_id : int,
                                 game_room : dict | None,
                                 in_game_list: list,
                                 connected_users : dict):
    # If the user is already in game, don't create the room
    if my_id in in_game_list:
        print("\nWS : User", my_id, "already in game", file=sys.stderr)
        return None

    # If game is already create, not create an other one
    if game_room != None:
        print("\nWS : User", my_id, "already have a local game room",
              file=sys.stderr)
        return game_room

    # create the room
    print("\nWS : User", my_id, "create a local game room", file=sys.stderr)
    game_room = {'map_id' : 0,
                 'power_up' : False,
                 'team_left' : list(),
                 'team_right' : list()
                }

    str_msg = create_game_room_status_message("createLocalRoomInfo", game_room)
    await send_msg_to_id(my_id, connected_users, str_msg)
    return game_room

async def quit_local_game_room(my_id:int,
                               connected_users:dict,
                               game_room:dict):
    # Check if the room exist
    if game_room == None:
        print("\nWS : User", my_id, "local room doesn't exist", file=sys.stderr)
        await send_error_to_id(my_id, connected_users, "Room doesn t exist")
        return None

    # Send to player in room that user leave it
    print("\nWS : User", my_id, "quit local game room", file=sys.stderr)
    str_msg = str({"type":"quitLocalGameRoom"}).replace("'", '"')
    await send_msg_to_id(my_id, connected_users, str_msg)

    return None


async def local_game_room_add_something(my_id:int,
                                        connected_users:dict,
                                        data:dict,
                                        game_room:dict,
                                        id_to_add:int):
    # Check if the room exist
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

    # Join left team
    if target_team == "left":
        # Check if team is full
        if len(game_room["team_left"]) >= MAX_PLAYER_PER_TEAM:
            print("\nWS : User", my_id, "Left team full", file=sys.stderr)
            await send_error_to_id(my_id, connected_users, "Left team full")
            return
        game_room["team_left"].append(id_to_add)

    # Join right team
    elif target_team == "right":
        # Check if team is full
        if len(game_room["team_right"]) >= MAX_PLAYER_PER_TEAM:
            print("\nWS : User", my_id, "Right team full", file=sys.stderr)
            await send_error_to_id(my_id, connected_users, "Right team full")
            return
        game_room["team_right"].append(id_to_add)

    else:
        # Team field is incorrect
        print("\nWS : User", my_id, "team is only left or right", file=sys.stderr)
        await send_error_to_id(my_id, connected_users,
                                "Team is only left or right")

    # Update message
    if id_to_add == -1:
        print("\nWS : User", my_id, "Bot add to team", target_team, file=sys.stderr)
    else:
        print("\nWS : User", my_id, "Player add to team", target_team,
              file=sys.stderr)
    str_msg = create_game_room_status_message("updateLocalRoomInfo", game_room)
    await send_msg_to_id(my_id, connected_users, str_msg)


async def local_game_room_remove_something(my_id:int,
                               connected_users:dict,
                               data:dict,
                               game_room:dict,
                               id_to_remove:int):
    # Check if the room exist
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

    # Join left team
    if target_team == "left":
        # Check if bot isn't in team
        if id_to_remove not in game_room["team_left"]:
            print("\nWS : User", my_id, "Left team have not bot", file=sys.stderr)
            await send_error_to_id(my_id, connected_users, "Left team have not bot")
            return
        game_room["team_left"].remove(id_to_remove)

    # Join right team
    elif target_team == "right":
        # Check if bot isn't in team
        if id_to_remove not in game_room["team_right"]:
            print("\nWS : User", my_id, "Right team have not bot", file=sys.stderr)
            await send_error_to_id(my_id, connected_users, "Right team have not bot")
            return
        game_room["team_right"].remove(id_to_remove)

    else:
        # Team field is incorrect
        print("\nWS : User", my_id, "team is only left or right", file=sys.stderr)
        await send_error_to_id(my_id, connected_users,
                                "Team is only left or right")

    # Update message
    if id_to_remove == IA_ID:
        print("\nWS : User", my_id, "Bot remove from team", target_team,
              file=sys.stderr)
    else:
        print("\nWS : User", my_id, "Player remove from team", target_team,
              file=sys.stderr)
    str_msg = create_game_room_status_message("updateLocalRoomInfo", game_room)
    await send_msg_to_id(my_id, connected_users, str_msg)


async def local_game_room_switch_power_up(my_id:int,
                                          connected_users:dict,
                                          game_room:dict):
    # Check if the room exist
    if game_room == None:
        print("\nWS : User", my_id, "room doesn't exist", file=sys.stderr)
        await send_error_to_id(my_id, connected_users, "Room doesn t exist")
        return

    game_room['power_up'] = not game_room['power_up']

    print("\nWS : User", my_id, "change power up to", game_room['power_up'],
          file=sys.stderr)
    # Update message
    str_msg = create_game_room_status_message("updateLocalRoomInfo", game_room)
    await send_msg_to_id(my_id, connected_users, str_msg)


async def local_game_room_change_map(my_id:int,
                                     connected_users:dict,
                                     data:dict,
                                     game_room:dict):
    # Check if the room exist
    if game_room == None:
        print("\nWS : User", my_id, "room doesn't exist", file=sys.stderr)
        await send_error_to_id(my_id, connected_users, "Room doesn t exist")
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
    str_msg = create_game_room_status_message("updateLocalRoomInfo", game_room)
    await send_msg_to_id(my_id, connected_users, str_msg)


async def local_game_room_start_game(my_id:int,
                                     connected_users:dict,
                                     game_room:dict,
                                     in_game_list:list):
    # Check if the room exist
    if game_room == None:
        print("\nWS : User", my_id, "local room doesn't exist",
              file=sys.stderr)
        await send_error_to_id(my_id, connected_users, "Local room doesn t exist")
        return None
    print("\nWS : User", my_id, "local room check ok", file=sys.stderr)

    if len(game_room['team_left']) == 0:
        print("\nWS : User", my_id, "Team left empty", file=sys.stderr)
        await send_error_to_id(my_id, connected_users, "Team left empty")
        return game_room
    print("\nWS : User", my_id, "team left check ok", file=sys.stderr)

    if len(game_room['team_right']) == 0:
        print("\nWS : User", my_id, "Team right empty", file=sys.stderr)
        await send_error_to_id(my_id, connected_users, "Team right empty")
        return game_room
    print("\nWS : User", my_id, "team right check ok", file=sys.stderr)

    if not is_game_server_free():
        print("\nWS : User", my_id, "No server free", file=sys.stderr)
        await send_error_to_id(my_id, connected_users, "No server free")
        return game_room
    print("\nWS : User", my_id, "game server free", file=sys.stderr)

    # team [int, int]
    # int per paddle, 0 for player, 1 for ia
    ret = await create_new_local_game(in_game_list, game_room["map_id"],
                                game_room["power_up"], game_room["team_left"],
                                game_room["team_right"], GAME_TYPE_LOCAL_CUSTOM)

    if ret == None:
        print("\nWS : ERROR : No game server free", file=sys.stderr)
        return game_room
    print("\nWS : User", my_id, "game server ok", file=sys.stderr)

    game_room = None

    str_msg = str({"type" : "LocalGameStart",
                   "gamePort" : ret[1],
                   "gameType" : GAME_TYPE_LOCAL_CUSTOM
                  }).replace("'", '"')
    await send_msg_to_id(my_id, connected_users, str_msg)
    return game_room
