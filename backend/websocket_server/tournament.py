import sys
import random
from websocket_server.utils import get_user_by_id, send_error_to_id, \
                                   send_msg_to_id, check_user_admin, \
                                   create_game_start_message, GAME_TYPE_TOURNAMENT, \
                                   NUMBER_OF_MAP, IA_ID
from websocket_server.message import message_in_general
from websocket_server.game_server_manager import create_new_game, is_game_server_free

MISSION_CONTROL = get_user_by_id(-2)

STATE_NO_TOURNAMENT = 0
STATE_CREATE_TOURNAMENT = 1
STATE_START_TOURNAMENT = 2
STATE_FINISH_TOURNAMENT = 3

tournament = {
    "state" : STATE_NO_TOURNAMENT,
    "mapId" : 0,
    "powerUp" : 0,
    "winner" : None,
    "final" : [None] * 2,
    "half" : [None] * 4,
    "quarter" : [None] * 8,
    "players" : [],
    "nicknames" : dict(),
    "matchRunning" : False
}

def get_user_view(user_id:int) -> list[int, str, str]:
    global tournament
    user = get_user_by_id(user_id)

    if user_id == -1:
        nickname = "bosco"
    else:
        nickname = tournament["nicknames"][user_id]

    return [user_id, user.profilPicture.name, nickname]


def get_lst_users_view() -> list:
    global tournament

    lst = []

    for id in tournament["players"]:
        lst.append(get_user_view(id))

    return lst


def get_next_match_tournament() -> tuple[int, int] | None:
    global tournament

    winner = tournament["winner"]
    final = tournament["final"]
    half = tournament["half"]
    quarter = tournament["quarter"]

    # Check if the tournament in finish
    if winner != None:
        return None

    # Check if next match is a quarter
    for i in range(len(half)):
        if half[i] == None:
            id_quarter_1 = i * 2
            id_quarter_2 = (i * 2) + 1
            return (quarter[id_quarter_1], quarter[id_quarter_2])

    # Check if next match is an half final
    for i in range(len(final)):
        if final[i] == None:
            id_half_1 = i * 2
            id_half_2 = (i * 2) + 1
            return (half[id_half_1], half[id_half_2])

    # Check if next match is the final
    return (final[0], final[1])


def get_next_match_user(user_id:int) -> tuple[int, int] | None:
    global tournament

    winner = tournament["winner"]
    final:list = tournament["final"]
    half:list = tournament["half"]
    quarter:list = tournament["quarter"]

    # Check if the tournament in finish
    if winner != None:
        return None

    quarter_index = quarter.index(user_id)
    half_index = quarter_index // 2

    # Next match is quarter
    if half[half_index] == None:
        quarter_index_1 = half_index * 2
        quarter_index_2 = (half_index * 2) + 1
        return (quarter[quarter_index_1], quarter[quarter_index_2])

    # If quarter match if lose
    if half[half_index] != user_id:
        return None

    final_index = half_index // 2

    # Next match is half final
    if final[final] == None:
        half_index_1 = final_index * 2
        half_index_2 = (final_index * 2) + 1
        return (half[half_index_1], half[half_index_2] )

    # If half final match is lose
    if final[final] != user_id:
        return None

    # This is the final
    return (final[0], final[1])


def create_tournament_state_msg():
    global tournament
    msg = {"type" : "tournamentState",
           "powerUp" : str(tournament["powerUp"]).lower(),
           "mapId" : tournament["mapId"],
           "players" : get_lst_users_view()}
    return str(msg).replace("'", '"')


def create_tournament_tree_msg():
    global tournament
    msg = {"type" : "tournamentTreeUpdate",
           "winner" : str(tournament["winner"]),
           "final" : str(tournament["final"]),
           "half" : str(tournament["half"]),
           "quarter" : str(tournament["quarter"]),
           }
    return str(msg).replace("None", "null").replace("'", '"')


async def create_tournament(my_id:int,
                            connected_users:dict):
    global tournament

    # Check if user is an admin
    if not await check_user_admin(my_id, connected_users):
        return

    # Check if there is a tournament not finish
    if tournament['state'] != STATE_NO_TOURNAMENT or \
        tournament['state'] != STATE_FINISH_TOURNAMENT:
        print("WS : User", my_id, "Tournament already create and not finish")
        await send_error_to_id(my_id, connected_users,
                         "Tournament already create and not finish")
        return

    tournament = {
        "state" : STATE_NO_TOURNAMENT,
        "mapId" : 0,
        "powerUp" : 0,
        "winner" : None,
        "final" : [None] * 2,
        "half" : [None] * 4,
        "quarter" : [None] * 8,
        "players" : [],
        "nicknames" : dict(),
        "matchRunning" : False
    }

    print("WS : User", my_id, "Tournament create !",file=sys.stderr)
    str_msg = create_tournament_state_msg()
    await send_msg_to_id(my_id, connected_users, str_msg)


async def switch_tournament_power_up(my_id:int,
                                     connected_users:dict):
    global tournament

    # Check if user is an admin
    if not await check_user_admin(my_id, connected_users):
        return

    # Check if the tournament isn't in creation
    if tournament["state"] != STATE_CREATE_TOURNAMENT:
        print("WS : User", my_id, "Tournament must be in creation to be modified")
        await send_error_to_id(my_id, connected_users,
                               "Tournament must be in creation to be modified")
        return

    # Switch power up
    tournament["powerUp"] = not tournament["powerUp"]

    # Update message
    print("WS : User", my_id, "Tournament switch power up", file=sys.stderr)
    str_msg = create_tournament_state_msg()
    await send_msg_to_id(my_id, connected_users, str_msg)
    for user_id in tournament["players"]:
        await send_msg_to_id(user_id, connected_users, str_msg)


async def modify_tournament_map_id(my_id:int,
                                     connected_users:dict,
                                     data:dict):
    global tournament

    # Check if user is an admin
    if not await check_user_admin(my_id, connected_users):
        return

    # get the map id field
    map_id = data.get("mapId", None)
    if map_id == None:
        print("WS : User", my_id, "Missing mapId field", file=sys.stderr)
        await send_error_to_id(my_id, connected_users, "Missing mapId field")
        return

    try:
        map_id = int(map_id)
    except:
        print("WS : User", my_id, "MapId need to be an interger", file=sys.stderr)
        await send_error_to_id(my_id, connected_users,
                               "MapId need to be an interger")
        return

    if map_id < 0 or map_id >= NUMBER_OF_MAP:
        print("WS : User", my_id, "MapId need to be between 0 and "
              + str(NUMBER_OF_MAP - 1), file=sys.stderr)
        await send_error_to_id(my_id, connected_users,
                               "MapId need to be between 0 and "
                               + str(NUMBER_OF_MAP - 1))
        return

    # Check if the tournament isn't in creation
    if tournament["state"] != STATE_CREATE_TOURNAMENT:
        print("WS : User", my_id, "Tournament must be in creation to be modified",
              file=sys.stderr)
        await send_error_to_id(my_id, connected_users,
                               "Tournament must be in creation to be modified")
        return

    # Change map id
    tournament["mapId"] = map_id

    # Update message
    print("WS : User", my_id, "Tournament change map id to", map_id,
          file=sys.stderr)
    str_msg = create_tournament_state_msg()
    await send_msg_to_id(my_id, connected_users, str_msg)
    for user_id in tournament["players"]:
        await send_msg_to_id(user_id, connected_users, str_msg)


async def start_tournament(my_id:int,
                           connected_users:dict,
                           in_game_list:list):
    global tournament

    # Check if user is an admin
    if not await check_user_admin(my_id, connected_users):
        return

    # Check if the tournament isn't in creation
    if tournament["state"] != STATE_CREATE_TOURNAMENT:
        print("WS : User", my_id, "Tournament must be in creation to be start",
              file=sys.stderr)
        await send_error_to_id(my_id, connected_users,
                               "Tournament must be in creation to be start")
        return

    # Check if threre is less than 2 players
    if len(tournament["players"]) < 2:
        print("WS : User", my_id, "Tournament must be have at least 2 player " \
              + " for begin", file=sys.stderr)
        await send_error_to_id(my_id, connected_users,
                               "Tournament must be have at least 2 player " \
                               + " for begin")
        return

    tournament["state"] = STATE_START_TOURNAMENT

    # Fill the fist step of tournament
    tournament["quarter"] = list()
    for player_id in tournament["players"]:
        tournament["quarter"].append(player_id)

    while len(tournament["quarter"]) < 8:
        tournament["quarter"].append(IA_ID)

    # shuffle this step
    random.shuffle(tournament["quarter"])

    # Server message to inform users that the tournament begin
    await message_in_general("The Tournament start !", MISSION_CONTROL,
                             connected_users)
    await tournament_next_start_match(connected_users, in_game_list)


async def tournament_next_start_match(connected_users:dict,
                                      in_game_list:list):
    global tournament

    # Check is the tournament is running
    if tournament["state"] != STATE_START_TOURNAMENT:
        print("WS : Tournament must be in running to launch a match",
              file=sys.stderr)
        return

    # Check if a macth is running
    if tournament["matchRunning"]:
        print("WS : Tournament can't run only one match at same time",
              file=sys.stderr)
        return

    # Get next match
    next_match = get_next_match_tournament()

    # Check if there is a next match
    if next_match == None:
        print("WS : No next match", file=sys.stderr)
        return

    # Check if we know the 2 player of next match
    if next_match[0] == None or next_match[1] == None:
        print("WS : At least one user", file=sys.stderr)
        return

    # Check if is a server free
    if not is_game_server_free():
        print("WS : No server free", file=sys.stderr)
        return

    # Create the game
    ret = await create_new_game(in_game_list, 0, False, [next_match[0]],
                                [next_match[1]], GAME_TYPE_TOURNAMENT)

    if ret == None:
        print("\nWS : ERROR : No game server free, put users", file=sys.stderr)
        return

    p1 = get_user_view(next_match[0])[2]
    p2 = get_user_view(next_match[1])[2]

    await message_in_general("New match beetwen " + p1 + " and " + p2,
                             MISSION_CONTROL, connected_users)

    tournament["matchRunning"] = True

    # Send start game message to first player in waitlist
    first_player_msg = create_game_start_message(ret[1], 0, 0, GAME_TYPE_TOURNAMENT)
    for websocket in connected_users.get(next_match[0], []):
        await websocket.send(first_player_msg)

    # Send start game message to current player
    current_player_msg = create_game_start_message(ret[1], 0, 1,
                                                   GAME_TYPE_TOURNAMENT)
    for websocket in connected_users.get(next_match[1], []):
        await websocket.send(current_player_msg)


async def tournament_end_match(winner:int,
                               connected_users:dict):
    global tournament

    # Check is the tournament is running
    if tournament["state"] != STATE_START_TOURNAMENT:
        print("WS : Tournament must be in running to end a match",
              file=sys.stderr)
        return

    nickname = get_user_view(winner)[2]

    if winner in tournament["final"]:
        tournament["matchRunning"] = False
        tournament["winner"] = winner
        tournament["state"] = STATE_FINISH_TOURNAMENT
        print("WS : Tournament end ! Winner is", winner, file=sys.stderr)
        await message_in_general("The winner of tournament is " + nickname,
                             MISSION_CONTROL, connected_users)
        return

    if winner in tournament["half"]:
        tournament["matchRunning"] = False
        index = tournament["half"].index(winner)
        index //= 2
        tournament["final"][index] = winner
        print("WS :", winner, " win the match !", file=sys.stderr)
        await message_in_general(nickname + "win the match !",
                             MISSION_CONTROL, connected_users)
        return

    if winner in tournament["quarter"]:
        tournament["matchRunning"] = False
        index = tournament["quarter"].index(winner)
        index //= 2
        tournament["half"][index] = winner
        print("WS :", winner, " win the match !", file=sys.stderr)
        await message_in_general(nickname + "win the match !",
                             MISSION_CONTROL, connected_users)
        return

    print("WS :", winner, "wtf who are you ?!", file=sys.stderr)


async def join_tournament(my_id:int,
                         connected_users:dict,
                         data:dict):
    global tournament

    # Check if the tournament isn't in creation
    if tournament["state"] != STATE_CREATE_TOURNAMENT:
        print("WS : User", my_id, "Tournament must be in creation to join it",
              file=sys.stderr)
        await send_error_to_id(my_id, connected_users,
                               "Tournament must be in creation to join it")
        return

    # Check if the tournament is full
    if len(tournament["players"]) >= 8:
        print("WS : User", my_id, "Tournament is full", file=sys.stderr)
        await send_error_to_id(my_id, connected_users, "Tournament is full")
        return

    # get nickname field
    nickname : str = data.get("nickname", None)
    if nickname == None:
        print("WS : User", my_id, "Missing nickname field", file=sys.stderr)
        await send_error_to_id(my_id, connected_users, "Missing nickname field")
        return

    if len(nickname) < 2 or len(nickname) > 15:
        print("WS : User", my_id,
              "Nickname need to be between 2 and 15 characters", file=sys.stderr)
        await send_error_to_id(my_id, connected_users,
                               "Nickname need to be between 2 and 15 characters")
        return

    # Check if nickname haven't bad caracters
    nickname = nickname.lower()
    good_chars = "abcdefghijklmnoprstuvwxyz0123456789_"
    for c in nickname:
        if c not in good_chars:
            print("WS : User", my_id, "Bad nickname. Only alphanum and "
                  + "underscore autorised", file=sys.stderr)
            await send_error_to_id(my_id, connected_users,
                                   "Bad nickname. Only alphanum and "
                                   + "underscore autorised")
            return

    # Check if nickname is unique
    if nickname in tournament["nicknames"] or nickname == "bosco":
        print("WS : User", my_id, "Nickname is already used", file=sys.stderr)
        await send_error_to_id(my_id, connected_users, "Nickname is already used")
        return

    tournament["players"].append(my_id)
    tournament["nicknames"][my_id] = nickname

    print("WS : User", my_id, "join tournament", file=sys.stderr)
    str_msg = str({"type" : "joinReply",
                   "powerUp" : str(tournament['powerUp']).lower(),
                   "mapId" : tournament["mapId"],
                   "players" : get_lst_users_view()
                 }).replace("'", '"')
    await send_msg_to_id(my_id, connected_users, str_msg)

    # Update player list for other user
    str_msg = str({"type" : "tournamentPlayersList",
                   "players" : get_lst_users_view()}).replace("'", '"')
    for id in tournament["players"]:
        if id != my_id:
            await send_msg_to_id(id, connected_users, str_msg)


async def quit_tournament(my_id:int,
                          connected_users:dict):
    global tournament

    # Check if the tournament isn't in creation
    if tournament["state"] != STATE_CREATE_TOURNAMENT:
        print("WS : User", my_id, "Tournament must be in creation to join it",
              file=sys.stderr)
        await send_error_to_id(my_id, connected_users,
                               "Tournament must be in creation to join it")
        return

    tournament["players"].remove(my_id)
    tournament["nicknames"].pop(my_id)
    print("WS : User", my_id, "quit tournament", file=sys.stderr)

    # Update player list for other user
    str_msg = str({"type" : "tournamentPlayersList",
                   "players" : get_lst_users_view()}).replace("'", '"')
    for id in tournament["players"]:
        if id != my_id:
            await send_msg_to_id(id, connected_users, str_msg)


async def get_tournament_info(my_id:int,
                                connected_users:dict):
    global tournament

    status = ['nothing', 'create', 'start', 'finish']
    str_msg = str({"type" : "tournamentInfo",
                   "status" : status[tournament["state"]],
                   "mapId" : tournament["mapId"],
                   "powerUp" : str(tournament["powerUp"]).lower()
                   }).replace("'", '"')
    await send_msg_to_id(my_id, connected_users, str_msg)


async def get_users_tournament(my_id:int,
                                connected_users:dict):
    global tournament

    str_msg = str({"type" : "tournamentPlayersList",
                   "players" : get_lst_users_view()}).replace("'", '"')
    await send_msg_to_id(my_id, connected_users, str_msg)


async def is_user_in_tournament(my_id:int,
                                connected_users:dict):
    global tournament

    str_msg = str({"type" : "InTournament",
                   "inTournament" : str(my_id in tournament["player"]).lower()
                   }).replace("'", '"')
    await send_msg_to_id(my_id, connected_users, str_msg)


async def next_match_tournament(my_id:int,
                                connected_users:dict):
    next_match = get_next_match_tournament()

    if next_match == None:
        match = "null"
    else:
        match = []
        for i in range(2):
            if next_match[i] == None:
                match.append("null")
            else:
                match.append(get_user_view(next_match[i]))

    str_msg = str({"type" : "nextMatch",
                "match" : match
                }).replace("'", '"')
    await send_msg_to_id(my_id, connected_users, str_msg)


async def next_match_user(my_id:int,
                          connected_users:dict):
    next_match = get_next_match_user(my_id)

    if next_match == None:
        match = "null"
    else:
        match = []
        for i in range(2):
            if next_match[i] == None:
                match.append("null")
            else:
                match.append(get_user_view(next_match[i]))

    str_msg = str({"type" : "nextMatch",
                "match" : match
                }).replace("'", '"')
    await send_msg_to_id(my_id, connected_users, str_msg)
