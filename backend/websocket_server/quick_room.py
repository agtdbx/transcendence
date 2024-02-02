import sys
from websocket_server.game_server_manager import create_new_game, is_game_server_free

waitlist = []

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
    if len(waitlist) == 0:
        waitlist.append(my_id)
        print("\nPut user", my_id, "in waitlist", file=sys.stderr)
        return

    if not is_game_server_free():
        waitlist.append(my_id)
        print("\nNo game server free, put user", my_id, "in waitlist", file=sys.stderr)
        return


    first_player_id = waitlist.pop(0)
    print("\nStart game beetween", my_id, "and", first_player_id, file=sys.stderr)

    # team [int, int]
    # int per paddle, 0 for player, 1 for ia
    ret = await create_new_game(0, False, [0], [0])

    if ret == None:
        waitlist.append(my_id)
        print("\nERROR : No game server free, put user", my_id, "in waitlist", file=sys.stderr)
        return

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
        print("\nRemove user", user_id, "of waitlist", file=sys.stderr)
        waitlist.remove(user_id)
