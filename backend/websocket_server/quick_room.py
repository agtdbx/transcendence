import sys
from websocket_server.game_server_manager import create_new_game, is_game_server_free

waitlist = []
in_game_list = []

def create_game_start_message(port, paddle_id, team_id):
    message : dict = {
        "type" : "gameStart",
        "gamePort" : str(port),
        "paddleId" : str(paddle_id),
        "teamId" : str(team_id)
    }
    str_message = str(message)
    str_message = str_message.replace("'", '"')

    return str_message


async def join_quick_room(my_id : int, connected_users : dict):
    # If the user is already in waitlist or in game, don't pu it in waitlist
    if my_id in waitlist or my_id in in_game_list:
        print("\nWS : User", my_id, "already in waitlist or in game", file=sys.stderr)
        return

    if len(waitlist) == 0:
        waitlist.append(my_id)
        print("\nWS : Put user", my_id, "in waitlist", file=sys.stderr)
        return

    if not is_game_server_free():
        waitlist.append(my_id)
        print("\nWS : No game server free, put user", my_id, "in waitlist", file=sys.stderr)
        return

    first_player_id = waitlist.pop(0)
    print("\nWS : Start game beetween", my_id, "and", first_player_id, file=sys.stderr)

    # team [int, int]
    # int per paddle, 0 for player, 1 for ia
    ret = await create_new_game(0, False, [0], [0], [my_id, first_player_id])

    if ret == None:
        waitlist.append(my_id)
        print("\nWS : ERROR : No game server free, put user", my_id, "in waitlist", file=sys.stderr)
        return

    in_game_list.append(first_player_id)
    in_game_list.append(my_id)

    # Send start game message to first player in waitlist
    first_player_msg = create_game_start_message(ret[1], 0, 0)
    for websocket in connected_users.get(first_player_id, []):
        await websocket.send(first_player_msg)

    # Send start game message to current player
    current_player_msg = create_game_start_message(ret[1], 0, 1)
    for websocket in connected_users.get(my_id, []):
        await websocket.send(current_player_msg)


def leave_quick_room(user_id):
    if user_id in waitlist:
        print("\nWS : Remove user", user_id, "of waitlist", file=sys.stderr)
        waitlist.remove(user_id)


async def check_if_can_start_new_game(data:dict, connected_users:dict):
    users_id = data.get("usersId", None)
    if users_id == None:
        print("\nWS : Missing info which user was in game :", data, file=sys.stderr)

    for id in users_id:
        if id in in_game_list:
            in_game_list.remove(id)

    if len(waitlist) <= 1:
        print("\nWS : No enough users in wait to start a game", file=sys.stderr)
        return

    if not is_game_server_free():
        print("\nWS : No game server free, no game start", file=sys.stderr)
        return

    first_player_id = waitlist.pop(0)
    second_player_id = waitlist.pop(0)
    print("\nWS : Start game beetween", first_player_id, "and", second_player_id, file=sys.stderr)

    ret = await create_new_game(0, False, [0], [0], [first_player_id, second_player_id])

    if ret == None:
        waitlist.append(first_player_id)
        waitlist.append(second_player_id)
        print("\nWS : ERROR : No game server free, put users", [first_player_id, second_player_id], "in waitlist", file=sys.stderr)
        return

    in_game_list.append(first_player_id)
    in_game_list.append(second_player_id)

    # Send start game message to first player in waitlist
    first_player_msg = create_game_start_message(ret[1], 0, 0)
    for websocket in connected_users.get(first_player_id, []):
        await websocket.send(first_player_msg)

    # Send start game message to current player
    current_player_msg = create_game_start_message(ret[1], 0, 1)
    for websocket in connected_users.get(second_player_id, []):
        await websocket.send(current_player_msg)
