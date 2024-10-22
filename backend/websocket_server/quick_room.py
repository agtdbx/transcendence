import sys
from websocket_server.utils import create_game_start_message, GAME_TYPE_QUICK
from websocket_server.game_server_manager import create_new_game, is_game_server_free


async def waitlist_message(type:str,
                     user_id:int,
                     waitlist:list,
                     connected_users:dict):
    if type == "join":
        waitlist.append(user_id)
        print("\nWS : Put user", user_id, "in waitlist", file=sys.stderr)
        msg = {'type' : 'joinWaitlist'}
    else:
        waitlist.remove(user_id)
        print("\nWS : Remove user", user_id, "of waitlist", file=sys.stderr)
        msg = {'type' : 'quitWaitlist'}

    str_msg = str(msg).replace("'", '"')
    for websocket in connected_users.get(user_id, []):
        await websocket.send(str_msg)


async def join_quick_room(my_id : int,
                          waitlist:list,
                          in_game_list: list,
                          connected_users : dict):
    # If the user is already in waitlist or in game, don't pu it in waitlist
    if my_id in waitlist or my_id in in_game_list:
        print("\nWS : User", my_id, "already in waitlist or in game",
              file=sys.stderr)
        return

    if len(waitlist) == 0:
        await waitlist_message("join", my_id, waitlist, connected_users)
        return

    if not is_game_server_free():
        await waitlist_message("join", my_id, waitlist, connected_users)
        return

    first_player_id = waitlist.pop(0)
    print("\nWS : Start game beetween", my_id, "and", first_player_id,
          file=sys.stderr)

    # team [int, int]
    # int per paddle, 0 for player, 1 for ia
    ret = await create_new_game(in_game_list, 0, False, [first_player_id], [my_id],
                                GAME_TYPE_QUICK)

    if ret == None:
        waitlist.append(first_player_id)
        waitlist.append(my_id)
        print("\nWS : ERROR : No game server free, put user", my_id, "in waitlist",
              file=sys.stderr)
        return

    # Send start game message to first player in waitlist
    first_player_msg = create_game_start_message(ret[1], 0, 0, GAME_TYPE_QUICK)
    for websocket in connected_users.get(first_player_id, []):
        await websocket.send(first_player_msg)

    # Send start game message to current player
    current_player_msg = create_game_start_message(ret[1], 0, 1, GAME_TYPE_QUICK)
    for websocket in connected_users.get(my_id, []):
        await websocket.send(current_player_msg)


async def leave_quick_room(user_id:int,
                           waitlist : list,
                           connected_users : dict):
    if user_id in waitlist:
        try:
            await waitlist_message("quit", user_id, waitlist, connected_users)
        except:
            pass


async def check_if_can_start_new_game(waitlist : list,
                                      in_game_list: list,
                                      connected_users:dict):
    if len(waitlist) <= 1:
        print("\nWS : No enough users in wait to start a game", file=sys.stderr)
        return

    if not is_game_server_free():
        print("\nWS : No game server free, no game start", file=sys.stderr)
        return

    first_player_id = waitlist.pop(0)
    second_player_id = waitlist.pop(0)
    print("\nWS : Start game beetween", first_player_id, "and", second_player_id,
          file=sys.stderr)

    ret = await create_new_game(in_game_list, 0, False, [first_player_id],
                                [second_player_id], GAME_TYPE_QUICK)

    if ret == None:
        waitlist.append(first_player_id)
        waitlist.append(second_player_id)
        print("\nWS : ERROR : No game server free, put users",
              [first_player_id, second_player_id], "in waitlist", file=sys.stderr)
        return

    # Send start game message to first player in waitlist
    first_player_msg = create_game_start_message(ret[1], 0, 0, GAME_TYPE_QUICK)
    for websocket in connected_users.get(first_player_id, []):
        await websocket.send(first_player_msg)

    # Send start game message to current player
    current_player_msg = create_game_start_message(ret[1], 0, 1, GAME_TYPE_QUICK)
    for websocket in connected_users.get(second_player_id, []):
        await websocket.send(current_player_msg)
