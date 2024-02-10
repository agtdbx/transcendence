from db_test.models import User

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
    users = User.objects.all().filter(idUser=user_id)
    if len(users) != 1:
        return None
    return users[0]


def get_user_by_username(username : str):
    users = User.objects.all().filter(username=username)
    if len(users) != 1:
        return None
    return users[0]
