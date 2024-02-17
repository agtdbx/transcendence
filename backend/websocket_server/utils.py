import sys
from db_test.models import User, Map, Link

def set_user_status(myid, status):
    user = User.objects.all().filter(idUser=myid)[0]
    user.status = status
    user.save()


async def send_error(websocket, error_explaination):
    error = {"type" : "error", "error" : error_explaination}
    str_error = str(error)
    str_error = str_error.replace("'", '"')
    await websocket.send(str_error)


def get_user_by_id(user_id : int):
    if user_id <= IA_ID:
        user_id = IA_ID
    users = User.objects.all().filter(idUser=user_id)
    if len(users) != 1:
        return None
    return users[0]


def get_user_by_username(username : str):
    users = User.objects.all().filter(username=username)
    if len(users) != 1:
        return None
    return users[0]


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


async def check_user_exist(my_id:int,
                           connected_users:dict) -> bool:
    user = get_user_by_id(my_id)
    # Check if user exist
    if user == None:
        print("WS : User", my_id, "didn't exist", file=sys.stderr)
        await send_error_to_id(my_id, connected_users, "User didn t exist")
        return False


GAME_TYPE_QUICK = 0
GAME_TYPE_CUSTOM = 1
GAME_TYPE_TOURNAMENT = 2
GAME_TYPE_LOCAL_CUSTOM = 3
GAME_TYPE_LOCAL_TOURNAMENT = 4

NUMBER_OF_MAP = 5
IA_ID = -1

def create_game_start_message(port:int,
                              paddle_id:int,
                              team_id:int,
                              type:int):
    message : dict = {
        "type" : "gameStart",
        "gamePort" : port,
        "paddleId" : paddle_id,
        "teamId" : team_id,
        "gameType" : type
    }
    str_message = str(message)
    str_message = str_message.replace("'", '"')

    return str_message


def get_map_name_by_id(map_id):
    maps = Map.objects.all().filter(idMap=map_id)
    if len(maps) != 1:
        return "Invalid map"
    return maps[0].name
