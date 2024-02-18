import sys
import random
import asyncio
from websocket_server.utils import get_user_by_id, send_error_to_id, \
                                   send_msg_to_id, get_map_name_by_id, \
                                   GAME_TYPE_LOCAL_TOURNAMENT, NUMBER_OF_MAP, IA_ID
from websocket_server.game_server_manager import create_new_local_game, \
                                                 is_game_server_free


STATE_NO_TOURNAMENT = 0
STATE_CREATE_TOURNAMENT = 1
STATE_START_TOURNAMENT = 2
STATE_FINISH_TOURNAMENT = 3


def get_user_view(my_id:int,
                  player_id:int,
                  tournament:dict) -> list[int, str, str]:
    if player_id <= IA_ID:
        user = get_user_by_id(IA_ID)
    else:
        user = get_user_by_id(my_id)

    if player_id <= IA_ID:
        nickname = "bosco " + str(-player_id)
    else:
        nickname = tournament["nicknames"][player_id]

    return [player_id, "/static/" + user.profilPicture.name, nickname]


def get_lst_users_view(my_id:int,
                       tournament:dict) -> list:
    lst = []

    for player_id in tournament["players"]:
        lst.append(get_user_view(my_id, player_id, tournament))

    return lst


def get_next_match_tournament(tournament:dict) -> tuple[int, int] | None:
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


def create_local_tournament_state_msg(my_id:int,
                                      tournament:dict):
    if tournament == None:
        msg = {"type" : "localTournamentState",
            "status" : STATE_NO_TOURNAMENT,
            "powerUp" : "false",
            "mapId" : 0,
            "mapName" : get_map_name_by_id(0),
            "players" : []}
    else:
        msg = {"type" : "localTournamentState",
            "status" : tournament["state"],
            "powerUp" : str(tournament["powerUp"]).lower(),
            "mapId" : tournament["mapId"],
            "mapName" : get_map_name_by_id(tournament["mapId"]),
            "players" : get_lst_users_view(my_id, tournament)}
    return str(msg).replace("'", '"')


def create_tournament_tree_msg(tournament:dict):
    players_grade = []
    for user_id in tournament["quarter"]:
        if user_id <= IA_ID:
            nickname = "bosco " + str(-user_id)
        else:
            nickname = tournament["nicknames"][user_id]

        if user_id == tournament["winner"]:
            players_grade.append([nickname, 3])
        elif user_id in tournament["final"]:
            players_grade.append([nickname, 2])
        elif user_id in tournament["half"]:
            players_grade.append([nickname, 1])
        else:
            players_grade.append([nickname, 0])

    msg = {"type" : "tournamentTreeUpdate",
           "playersGrade" : players_grade}
    return str(msg).replace("None", "null").replace("'", '"')


def get_last_tournament_score(player_id:int,
                              tournament:int) -> int:
    matchs = tournament["matchResults"]

    # For each user match, get it's match
    for i in range(len(matchs) - 1, -1, -1):
        # (player 1, player 2, score 1, score 2)
        match = matchs[i]

        if player_id == match[0]:
            return match[2]
        elif player_id == match[1]:
            return match[3]

    return -1


def create_tournament_winners_msg(my_id:int,
                                  type:str,
                                  tournament:dict):
    winner_id = tournament["winner"]
    second_id = None
    for user_id in tournament["final"]:
        if user_id != winner_id:
            second_id = user_id

    third_ids = []
    for user_id in tournament["half"]:
        if user_id != winner_id and user_id != second_id:
            third_ids.append(user_id)

    third_id = third_ids[1]
    if get_last_tournament_score(third_ids[0], tournament) > \
        get_last_tournament_score(third_ids[1], tournament):
        third_id = third_ids[0]

    msg = {"type" : type,
           "onePongMan" : get_user_view(my_id, winner_id, tournament),
           "second" : get_user_view(my_id, second_id, tournament),
           "third" : get_user_view(my_id, third_id, tournament)
           }
    return str(msg).replace("None", "null").replace("'", '"')


async def create_local_tournament(my_id:int,
                                  connected_users:dict,
                                  tournament:dict):
    if tournament == None:
        pass
    # Check if there is a tournament not finish
    elif tournament['state'] != STATE_NO_TOURNAMENT and \
        tournament['state'] != STATE_FINISH_TOURNAMENT:
        print("WS : User", my_id, "Tournament already create and not finish")
        await send_error_to_id(my_id, connected_users,
                         "Tournament already create and not finish")
        return tournament

    tournament = {
        "state" : STATE_CREATE_TOURNAMENT,
        "mapId" : 0,
        "powerUp" : False,
        "winner" : None,
        "final" : [None] * 2,
        "half" : [None] * 4,
        "quarter" : [None] * 8,
        "players" : [],
        "nicknames" : dict(),
        "matchRunning" : False,
        "matchResults" : [] # (player 1, player 2, score 1, score 2)
    }

    print("WS : User", my_id, "Local tournament create !",file=sys.stderr)

    # Update tournament info
    str_msg = create_local_tournament_state_msg(my_id, tournament)
    await send_msg_to_id(my_id, connected_users, str_msg)
    return tournament


async def local_tournament_add_player(my_id:int,
                                      connected_users:dict,
                                      tournament:dict,
                                      data:dict):
    # Check if the tournament isn't in creation
    if tournament == None or tournament["state"] != STATE_CREATE_TOURNAMENT:
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

    if len(nickname) < 1 or len(nickname) > 15:
        print("WS : User", my_id,
              "Nickname need to be between 1 and 15 characters", file=sys.stderr)
        await send_error_to_id(my_id, connected_users,
                               "Nickname need to be between 2 and 15 characters")
        return

    # Check if nickname haven't bad caracters
    nickname = nickname.lower()
    good_chars = "abcdefghijklmnopqrstuvwxyz0123456789_-"
    for c in nickname:
        if c not in good_chars:
            print("WS : User", my_id, "Bad nickname. Only alphanum and "
                  + "underscore autorised", file=sys.stderr)
            await send_error_to_id(my_id, connected_users,
                                   "Bad nickname. Only alphanum and "
                                   + "underscore autorised")
            return

    # Check if nickname is unique
    if nickname in tournament["nicknames"].values() or nickname == "bosco":
        print("WS : User", my_id, "Nickname", nickname, "is already used",
              file=sys.stderr)
        await send_error_to_id(my_id, connected_users, "Nickname " +
                               nickname + " is already used")
        return

    player_id = 1
    while player_id in tournament["players"]:
        player_id += 1

    tournament["players"].append(player_id)
    tournament["nicknames"][player_id] = nickname

    # Update tournament info
    str_msg = create_local_tournament_state_msg(my_id, tournament)
    await send_msg_to_id(my_id, connected_users, str_msg)


async def local_tournament_remove_player(my_id:int,
                                         connected_users:dict,
                                         tournament:dict,
                                         data:dict):
    print("WS : User", my_id, "try to remove player", file=sys.stderr)
    # Check if the tournament isn't in creation
    if tournament == None or tournament["state"] != STATE_CREATE_TOURNAMENT:
        print("WS : User", my_id, "Tournament must be in creation to join it",
              file=sys.stderr)
        await send_error_to_id(my_id, connected_users,
                               "Tournament must be in creation to join it")
        return

    # get nickname field
    nickname : str = data.get("nickname", None)
    if nickname == None:
        print("WS : User", my_id, "Missing nickname field", file=sys.stderr)
        await send_error_to_id(my_id, connected_users, "Missing nickname field")
        return

    player_id = None
    for test_id, test_nickname in tournament["nicknames"].items():
        print("WS : test (", test_id, ")", test_nickname, "==",
              nickname, file=sys.stderr)
        if test_nickname == nickname:
            player_id = test_id
            break

    # check if nickname is in tournament
    if player_id == None:
        print("WS : User", my_id, "Player", nickname,
              "not in local tournament", file=sys.stderr)
        await send_error_to_id(my_id, connected_users, "Player not in tournament")
        return

    tournament["players"].remove(player_id)
    tournament["nicknames"].pop(player_id)
    print("WS : User", my_id, "remove player", nickname, file=sys.stderr)

    # Update player list for other user
    # Update tournament info
    str_msg = create_local_tournament_state_msg(my_id, tournament)
    await send_msg_to_id(my_id, connected_users, str_msg)


async def switch_local_tournament_power_up(my_id:int,
                                           connected_users:dict,
                                           tournament:dict):
    # Check if the tournament isn't in creation
    if tournament == None or tournament["state"] != STATE_CREATE_TOURNAMENT:
        print("WS : User", my_id,
              "Local tournament must be in creation to be modified")
        await send_error_to_id(my_id, connected_users,
                               "Local tournament must be in creation to be modified")
        return

    # Switch power up
    tournament["powerUp"] = not tournament["powerUp"]

    # Update message
    print("WS : User", my_id, "Local tournament switch power up", file=sys.stderr)
    str_msg = create_local_tournament_state_msg(my_id, tournament)
    await send_msg_to_id(my_id, connected_users, str_msg)


async def modify_local_tournament_map_id(my_id:int,
                                         connected_users:dict,
                                         tournament:dict,
                                         data:dict):
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
    if tournament == None or tournament["state"] != STATE_CREATE_TOURNAMENT:
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
    str_msg = create_local_tournament_state_msg(my_id, tournament)
    await send_msg_to_id(my_id, connected_users, str_msg)


async def start_local_tournament(my_id:int,
                                 connected_users:dict,
                                 in_game_list:list,
                                 tournament:dict):
    # Check if the tournament isn't in creation
    if tournament == None or tournament["state"] != STATE_CREATE_TOURNAMENT:
        print("WS : User", my_id, "Local tournament must be in creation to be start",
              file=sys.stderr)
        await send_error_to_id(my_id, connected_users,
                               "Tournament must be in creation to be start")
        return

    # Check if threre is less than 2 players
    if len(tournament["players"]) < 2:
        print("WS : User", my_id, "Local tournament must be have at least 2 player "\
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
        tournament["quarter"].append(-len(tournament["quarter"]))

    # shuffle this step
    random.shuffle(tournament["quarter"])

    # Update message
    str_msg = create_local_tournament_state_msg(my_id, tournament)
    await send_msg_to_id(my_id, connected_users, str_msg)

    # Update tournament tree
    str_msg = create_tournament_tree_msg(tournament)
    await send_msg_to_id(my_id, connected_users, str_msg)

    print("WS : User", my_id, "Local tournament start !!", file=sys.stderr)
    asyncio.create_task(local_tournament_next_start_match(my_id,
                                                          connected_users,
                                                          in_game_list,
                                                          tournament))


async def local_tournament_next_start_match(my_id:int,
                                            connected_users:dict,
                                            in_game_list:list,
                                            tournament:dict):
    print("WS : TEST", tournament["state"],
              file=sys.stderr)

    # Check is the tournament is running
    if tournament == None or tournament["state"] != STATE_START_TOURNAMENT:
        print("WS : Local tournament must be in running to launch a match",
              file=sys.stderr)
        return

    # Check if a macth is running
    if tournament["matchRunning"]:
        print("WS : Local tournament can't run only one match at same time",
              file=sys.stderr)
        return

    # Get next match
    next_match = get_next_match_tournament(tournament)

    # Check if there is a next match
    if next_match == None:
        print("WS : No next match", file=sys.stderr)
        return

    # Check if we know the 2 player of next match
    if next_match[0] == None or next_match[1] == None:
        print("WS : At least one user is unkown", file=sys.stderr)
        return

    # If all participant are ia, end instantly the match
    if next_match[0] <= IA_ID and next_match[1] <= IA_ID:
        print("\nWS : Local tournament BOT vs BOT", file=sys.stderr)
        if random.randint(0, 1) == 0:
            winner = (4, next_match[0], 11, 0, my_id)
            await local_tournament_end_match(winner, connected_users,
                                             tournament)
        else:
            winner = (4, next_match[1], 0, 11, my_id)
            await local_tournament_end_match(winner, connected_users,
                                             tournament)
        await local_tournament_next_start_match(my_id, connected_users, in_game_list,
                                                tournament)
        return

    if next_match[0] <= IA_ID:
        user_right = get_user_by_id(my_id)
        # Check if the user if connected
        if user_right.status != 1:
            print("WS : User", user_right.username, "isn't connected",
                  file=sys.stderr)
            winner = (4, next_match[0], 11, 0, my_id)
            await local_tournament_end_match(winner, connected_users,
                                             tournament)
            await local_tournament_next_start_match(my_id, connected_users,
                                                    in_game_list, tournament)
            return

    elif next_match[1] <= IA_ID:
        user_left = get_user_by_id(my_id)
        # Check if the user if connected
        if user_left.status != 1:
            print("WS : User", user_left.username, "isn't connected",
                  file=sys.stderr)
            winner = (4, next_match[1], 0, 11, my_id)
            await local_tournament_end_match(winner, connected_users,
                                             tournament)
            await local_tournament_next_start_match(my_id, connected_users,
                                                    in_game_list, tournament)
            return

    else:
        print("\nWS : Local tournament match ready", file=sys.stderr)
        user_left = get_user_by_id(my_id)
        user_right = get_user_by_id(my_id)

        # If both user aren't connected, the winner is random
        if user_left.status != 1 and user_right.status != 1:
            print("WS : Both users aren't connected", file=sys.stderr)
            if random.randint(0, 1) == 0:
                winner = (4, next_match[0], 11, 0, my_id)
                await local_tournament_end_match(winner, connected_users,
                                                 tournament)
                await local_tournament_next_start_match(my_id, connected_users,
                                                        in_game_list, tournament)
                return
            else:
                winner = (4, next_match[1], 0, 11, my_id)
                await local_tournament_end_match(winner, connected_users,
                                                 tournament)
                await local_tournament_next_start_match(my_id, connected_users,
                                                        in_game_list, tournament)
                return

        # User left not conneted
        elif user_left.status != 1:
            print("WS : User", user_left.username, "isn't connected",
                  file=sys.stderr)
            winner = (4, next_match[1], 0, 11, my_id)
            await local_tournament_end_match(winner, connected_users,
                                             tournament)
            await local_tournament_next_start_match(my_id, connected_users,
                                                    in_game_list, tournament)
            return

        # User right not conneted
        elif user_right.status != 1:
            print("WS : User", user_right.username, "isn't connected",
                  file=sys.stderr)
            winner = (4, next_match[0], 11, 0, my_id)
            await local_tournament_end_match(winner, connected_users,
                                             tournament)
            await local_tournament_next_start_match(my_id, connected_users,
                                                    in_game_list, tournament)
            return

    # Check if is a server free
    if not is_game_server_free():
        print("WS : No server free", file=sys.stderr)
        return

    print("\nWS : Next match to start :", next_match, file=sys.stderr)

    # Create the game
    ret = await create_new_local_game(my_id, in_game_list, tournament["mapId"],
                                      tournament["powerUp"],
                                      [next_match[0]], [next_match[1]],
                                      GAME_TYPE_LOCAL_TOURNAMENT)

    if ret == None:
        print("\nWS : ERROR : No game server free, put users", file=sys.stderr)
        return

    # Update tournament tree
    str_msg = create_tournament_tree_msg(tournament)
    await send_msg_to_id(my_id, connected_users, str_msg)

    # Send next match to everyone
    next_match_test = get_next_match_tournament(tournament)

    if next_match_test == None:
        match = "null"
    else:
        match = []
        for i in range(2):
            if next_match_test[i] == None:
                match.append("null")
            else:
                match.append(get_user_view(my_id, next_match_test[i], tournament))

    str_msg = str({"type" : "nextMatch",
                "match" : match
                }).replace("'", '"')
    await send_msg_to_id(my_id, connected_users, str_msg)

    tournament["matchRunning"] = True

    await asyncio.sleep(10)

    # Send start game message to host
    str_msg = str({"type" : "LocalGameStart",
                            "gamePort" : ret[1],
                            "gameType" : GAME_TYPE_LOCAL_TOURNAMENT
                            }).replace("'", '"')
    await send_msg_to_id(my_id, connected_users, str_msg)


async def local_tournament_end_match(winner:tuple[int, int, int, int, int],
                                     connected_users:dict,
                                     tournament:dict):
    print("\nWS : Local tournament end match with winner :", winner, file=sys.stderr)
    # Check is the tournament is running
    if tournament == None or tournament["state"] != STATE_START_TOURNAMENT:
        print("WS : Local tournament must be in running to end a match",
              file=sys.stderr)
        for user_id in connected_users.keys():
            str_msg = create_local_tournament_state_msg(user_id, tournament)
            await send_msg_to_id(user_id, connected_users, str_msg)
        return

    winner_id = winner[1]

    if winner_id in tournament["final"]:
        id_p1 = tournament["final"][0]
        id_p2 = tournament["final"][1]
        matchResult = (id_p1, id_p2, winner[2], winner[3])
        print("WS : Match result :", matchResult, file=sys.stderr)
        tournament["matchResults"].append(matchResult)
        tournament["matchRunning"] = False
        tournament["winner"] = winner_id
        tournament["state"] = STATE_FINISH_TOURNAMENT
        print("WS : Local tournament end ! Winner is", winner_id, file=sys.stderr)
        str_msg = create_tournament_winners_msg(winner[4], "localEndTournament",
                                                tournament)
        for user_id in connected_users.keys():
            await send_msg_to_id(user_id, connected_users, str_msg)
        return

    if winner_id in tournament["half"]:
        tournament["matchRunning"] = False
        index = tournament["half"].index(winner_id)
        index //= 2
        tournament["final"][index] = winner_id
        id_p1 = tournament["half"][index * 2]
        id_p2 = tournament["half"][index * 2 + 1]
        matchResult = (id_p1, id_p2, winner[2], winner[3])
        print("WS : Match result :", matchResult, file=sys.stderr)
        tournament["matchResults"].append(matchResult)
        print("WS :", winner_id, " win the match !", file=sys.stderr)
        return

    if winner_id in tournament["quarter"]:
        tournament["matchRunning"] = False
        index = tournament["quarter"].index(winner_id)
        index //= 2
        tournament["half"][index] = winner_id
        id_p1 = tournament["quarter"][index * 2]
        id_p2 = tournament["quarter"][index * 2 + 1]
        matchResult = (id_p1, id_p2, winner[2], winner[3])
        print("WS : Match result :", matchResult, file=sys.stderr)
        tournament["matchResults"].append(matchResult)
        print("WS :", winner_id, " win the match !", file=sys.stderr)
        return

    print("WS :", winner_id, "wtf who are you ?!", file=sys.stderr)


async def get_local_tournament_info(my_id:int,
                                    connected_users:dict,
                                    tournament:dict):
    str_msg = create_local_tournament_state_msg(my_id, tournament)
    await send_msg_to_id(my_id, connected_users, str_msg)


async def get_local_tournament_tree(my_id:int,
                                    connected_users:dict,
                                    tournament:dict):
    # check if tournament is started
    if tournament == None or tournament['state'] != STATE_START_TOURNAMENT and \
        tournament['state'] != STATE_FINISH_TOURNAMENT:
        print("WS : User", my_id, "Tournament must be started to have a tree",
              file=sys.stderr)
        await send_error_to_id(my_id, connected_users,
                               "Tournament must be started to have a tree")
        return

    # Reply
    str_msg = create_tournament_tree_msg(tournament)
    await send_msg_to_id(my_id, connected_users, str_msg)


async def next_match_local_tournament(my_id:int,
                                      connected_users:dict,
                                      tournament:dict):
    # If tournament state is not started
    if tournament == None or tournament["state"] != STATE_START_TOURNAMENT:
        print("WS : User", my_id,
              "Tournament must be start to know the next match", file=sys.stderr)
        await send_error_to_id(my_id, connected_users,
                               "Tournament must be start to know the next match")
        return

    next_match = get_next_match_tournament(tournament)

    if next_match == None:
        match = "null"
    else:
        match = []
        for i in range(2):
            if next_match[i] == None:
                match.append("null")
            else:
                match.append(get_user_view(my_id, next_match[i], tournament))

    str_msg = str({"type" : "nextMatch",
                "match" : match
                }).replace("'", '"')
    await send_msg_to_id(my_id, connected_users, str_msg)


async def get_local_tournament_winners(my_id:int,
                                       connected_users:dict,
                                       tournament:dict):
    # If tournament state is not finish
    if tournament == None or tournament["state"] != STATE_FINISH_TOURNAMENT:
        print("WS : User", my_id,
              "Local tournament must be finish to know winners",
              file=sys.stderr)
        await send_error_to_id(my_id, connected_users,
                               "Local tournament must be finish to know winners")
        return

    str_msg = create_tournament_winners_msg(my_id, "winnersLocalTournament",
                                            tournament)
    await send_msg_to_id(my_id, connected_users, str_msg)
