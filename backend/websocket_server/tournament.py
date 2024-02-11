import sys
import random
from websocket_server.utils import get_user_by_id
from websocket_server.game_room import send_error_to_id, send_msg_to_id, \
                                        NUMBER_OF_MAP, IA_ID
from websocket_server.message import message_in_general

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
    "nicknames" : dict()
}

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


def get_next_match_userT(user_id:int) -> tuple[int, int] | None:
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


async def check_user_admin(my_id:int,
                            connected_users:dict) -> bool:
    user = get_user_by_id(my_id)
    # Check if user exist
    if user == None:
        print("WS : User", my_id, "didn't exist", file=sys.stderr)
        await send_error_to_id(my_id, connected_users, "User didn t exist")
        return False

    # Check if user is an admin
    if user.type != 2:
        print("WS : User", my_id, "Isn't an admin", file=sys.stderr)
        await send_error_to_id(my_id, connected_users,
                               "You need to be an administator")
        return False

    return True


def create_tournament_state_msg():
    global tournament
    msg = {"type" : "tournamentState",
           "powerUp" : str(tournament["powerUp"]).lower(),
           "mapId" : tournament["mapId"],
           "player" : tournament["players"]}
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
        "player" : [],
        "nicknames" : dict()
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
                           connected_users:dict):
    global current_id_tournament, tournament

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
    await message_in_general("The " + (current_id_tournament + 1) +
                             " Tournament start !",
                             MISSION_CONTROL, connected_users)

    # TODO : CONTINUEZ ! FAIRE UNE FONCTION QUI AVANCE L'ETAT DU TOURNOIS A CHAQUE
    #        FIN DE MATCH QUI EST UN MATCH DE TOURNOIS. DONC FAIRE EN SORTE DE
    #        DIFFÉRENCIER LES MATCHS DE TOURNOIS DES AUTRES ! PRIORITÉ AU TOURNOIS
    #        SUR LES QUICK GAMES !


async def joinTournament(my_id:int,
                         connected_users:dict,
                         data:dict):
    global idUserTournament, tournament

    # Check if the tournament isn't in creation
    if tournament["state"] != STATE_CREATE_TOURNAMENT:
        print("WS : User", my_id, "Tournament must be in creation to join it",
              file=sys.stderr)
        await send_error_to_id(my_id, connected_users,
                               "Tournament must be in creation to join it")
        return

    user = get_user_by_id(my_id)
    # Check if user exist
    if user == None:
        print("WS : User", my_id, "didn't exist", file=sys.stderr)
        await send_error_to_id(my_id, connected_users, "User didn t exist")
        return False

    # Check if the tournament is full
    if len(tournament["players"]) >= 8:
        print("WS : User", my_id, "Tournament is full", file=sys.stderr)
        await send_error_to_id(my_id, connected_users, "Tournament is full")
        return

    # get nickname field
    nickname = data.get("nickname", None)
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

    # Check if nickname is unique
    if nickname in tournament["nicknames"]:
        print("WS : User", my_id, "Nickname is already used", file=sys.stderr)
        await send_error_to_id(my_id, connected_users, "Nickname is already used")
        return

    tournament["players"].append(my_id)
    tournament["nicknames"][my_id] = nickname

    print("WS : User", my_id, "join tournament", file=sys.stderr)
    str_msg = str({"type" : "joinReply",
                   "powerUp" : str(tournament['powerUp']).lower(),
                   "mapId" : tournament["mapId"],
                   "players" : tournament["players"]
                 }).replace("'", '"')
    await send_msg_to_id(my_id, connected_users, str_msg)


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

    user = get_user_by_id(my_id)
    # Check if user exist
    if user == None:
        print("WS : User", my_id, "didn't exist", file=sys.stderr)
        await send_error_to_id(my_id, connected_users, "User didn t exist")
        return False

    tournament["players"].remove(my_id)
    tournament["nicknames"].pop(my_id)
    print("WS : User", my_id, "quit tournament", file=sys.stderr)
