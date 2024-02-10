import random
from db_test.models import User, UserTournament, Tournament
from websocket_server.utils import get_user_by_id
from websocket_server.game_room import send_error_to_id, send_msg_to_id, \
                                        NUMBER_OF_MAP, IA_ID
from websocket_server.message import message_in_general

MISSION_CONTROL = get_user_by_id(-2)

STATE_NO_TOURNAMENT = 0
STATE_CREATE_TOURNAMENT = 1
STATE_START_TOURNAMENT = 2
STATE_FINISH_TOURNAMENT = 3

current_id_tournament = None

tournament = {
    "state" : STATE_NO_TOURNAMENT,
    "mapId" : 0,
    "powerUp" : 0,
    "winner" : None,
    "final" : [None] * 2,
    "half" : [None] * 4,
    "quarter" : [None] * 8,
    "player" : []
}


async def check_user_admin(my_id:int,
                            connected_users:dict) -> bool:
    user = get_user_by_id(my_id)
    # Check if user exist
    if user == None:
        print("WS : User", my_id, "didn't exist")
        await send_error_to_id(my_id, connected_users, "User didn t exist")
        return False

    # Check if user is an admin
    if user.type != 2:
        print("WS : User", my_id, "Isn't an admin")
        await send_error_to_id(my_id, connected_users,
                               "You need to be an administator")
        return False

    return True


async def get_db_tournament(my_id:int,
                            connected_users:dict) -> Tournament | None:
    global current_id_tournament

    # Get the tournament in db
    test = Tournament.objects.all().filter(idTournament=current_id_tournament)

    if len(test) != 1:
        print("WS : User", my_id, "Tournament not found in db")
        await send_error_to_id(my_id, connected_users,
                               "Tournament not found in db")
        return None

    return test[0]


def create_tournament_state_msg():
    global tournament
    msg = {"type" : "tournamentState",
           "powerUp" : str(tournament["powerUp"]).lower(),
           "mapId" : tournament["mapId"],
           "player" : tournament["player"]}
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
    global current_id_tournament, tournament

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

    id_tournament = Tournament.objects.all().count()
    try:
        db_tournament = Tournament.objects.create(idTournament=id_tournament,
                                               state=STATE_CREATE_TOURNAMENT,
                                               idMap=0,
                                               powerUp=False)
        db_tournament.save()
    except Exception as error:
        print("WS : User", my_id, "Tournament creation error :", error)
        await send_error_to_id(my_id, connected_users,
                         "Tournament creation error")
        return

    tournament = {
        "state" : STATE_NO_TOURNAMENT,
        "mapId" : 0,
        "powerUp" : 0,
        "winner" : None,
        "final" : [None] * 2,
        "half" : [None] * 4,
        "quarter" : [None] * 8,
        "player" : []
    }

    current_id_tournament = id_tournament
    print("WS : User", my_id, "Tournament", id_tournament, "create !", error)
    str_msg = create_tournament_state_msg()
    await send_msg_to_id(my_id, connected_users, str_msg)


async def switch_tournament_power_up(my_id:int,
                                     connected_users:dict):
    global current_id_tournament, tournament

    # Check if user is an admin
    if not await check_user_admin(my_id, connected_users):
        return

    # Check if the tournament isn't in creation
    if tournament["state"] != STATE_CREATE_TOURNAMENT:
        print("WS : User", my_id, "Tournament must be in creation to be modified")
        await send_error_to_id(my_id, connected_users,
                               "Tournament must be in creation to be modified")
        return

    # Get the tournament in db
    db_tournament = await get_db_tournament(my_id, connected_users)
    if db_tournament == None:
        return

    # Switch power up
    tournament["powerUp"] = not tournament["powerUp"]

    try:
        db_tournament.powerUp = tournament["powerUp"]
        db_tournament.save()
    except Exception as error:
        print("WS : User", my_id, "Tournament db error :", error)
        await send_error_to_id(my_id, connected_users, "Tournament db error")
        return

    # Update message
    print("WS : User", my_id, "Tournament", current_id_tournament,
          "switch power up", error)
    str_msg = create_tournament_state_msg()
    await send_msg_to_id(my_id, connected_users, str_msg)
    for user_id in tournament["player"]:
        await send_msg_to_id(user_id, connected_users, str_msg)


async def modify_tournament_map_id(my_id:int,
                                     connected_users:dict,
                                     data:dict):
    global current_id_tournament, tournament

    # Check if user is an admin
    if not await check_user_admin(my_id, connected_users):
        return

    # get the map id field
    map_id = data.get("mapId", None)
    if map_id == None:
        print("WS : User", my_id, "Missing mapId field")
        await send_error_to_id(my_id, connected_users, "Missing mapId field")
        return

    try:
        map_id = int(map_id)
    except:
        print("WS : User", my_id, "MapId need to be an interger")
        await send_error_to_id(my_id, connected_users,
                               "MapId need to be an interger")
        return

    if map_id < 0 or map_id >= NUMBER_OF_MAP:
        print("WS : User", my_id, "MapId need to be between 0 and "
              + str(NUMBER_OF_MAP - 1))
        await send_error_to_id(my_id, connected_users,
                               "MapId need to be between 0 and "
                               + str(NUMBER_OF_MAP - 1))
        return

    # Check if the tournament isn't in creation
    if tournament["state"] != STATE_CREATE_TOURNAMENT:
        print("WS : User", my_id, "Tournament must be in creation to be modified")
        await send_error_to_id(my_id, connected_users,
                               "Tournament must be in creation to be modified")
        return

    # Get the tournament in db
    db_tournament = await get_db_tournament(my_id, connected_users)
    if db_tournament == None:
        return

    # Change map id
    tournament["mapId"] = map_id

    try:
        db_tournament.idMap = tournament["mapId"]
        db_tournament.save()
    except Exception as error:
        print("WS : User", my_id, "Tournament db error :", error)
        await send_error_to_id(my_id, connected_users, "Tournament db error")
        return

    # Update message
    print("WS : User", my_id, "Tournament", current_id_tournament,
          "switch power up", error)
    str_msg = create_tournament_state_msg()
    await send_msg_to_id(my_id, connected_users, str_msg)
    for user_id in tournament["player"]:
        await send_msg_to_id(user_id, connected_users, str_msg)


async def start_tournament(my_id:int,
                                     connected_users:dict):
    global current_id_tournament, tournament

    # Check if user is an admin
    if not await check_user_admin(my_id, connected_users):
        return

    # Check if the tournament isn't in creation
    if tournament["state"] != STATE_CREATE_TOURNAMENT:
        print("WS : User", my_id, "Tournament must be in creation to be start")
        await send_error_to_id(my_id, connected_users,
                               "Tournament must be in creation to be start")
        return

    # Get the tournament in db
    db_tournament = await get_db_tournament(my_id, connected_users)
    if db_tournament == None:
        return

    # Check if threre is less than 2 players
    if len(tournament["player"]) < 2:
        print("WS : User", my_id, "Tournament must be have at least 2 player " \
              + " for begin")
        await send_error_to_id(my_id, connected_users,
                               "Tournament must be have at least 2 player " \
                               + " for begin")
        return

    tournament["state"] = STATE_START_TOURNAMENT

    # Fill the fist step of tournament
    tournament["quarter"] = list()
    for player_id in tournament["player"]:
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

