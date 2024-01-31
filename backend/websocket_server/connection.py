import jwt, hashlib
from backend.settings import SECRET_KEY
from db_test.models import User, connectionPassword


async def send_reply_connection(websocket, success_value, error = ""):
    reply = {"type" : "connectionReply", "success" : str(success_value).lower(),
             "error" : error}
    str_reply = str(reply)
    str_reply = str_reply.replace("'", '"')
    await websocket.send(str_reply)


async def connection_by_token(websocket, data:dict) -> int | None:
    token = data.get('token', None)

    if token == None:
        await send_reply_connection(websocket, False, "Missing token field")
        return None

    jwtData = jwt.decode(token, SECRET_KEY, algorithms="HS256")
    if jwtData == None:
        await send_reply_connection(websocket, False, "Invalid token")
        return None

    user_id = jwtData.get("userId", None)
    if user_id == None:
        await send_reply_connection(websocket, False, "Invalid user id")
        return None

    users = User.objects.all().filter(idUser=user_id)
    if len(users) != 1:
        await send_reply_connection(websocket, False, "User not found")
        return None

    await send_reply_connection(websocket, True)
    return user_id


async def connection_by_username(websocket, data:dict) -> int | None:
    username : str = data.get('username', None)
    password : str = data.get('password', None)

    if username == None or password == None:
        await send_reply_connection(websocket, False, "Missing username or password field")
        return None

    users = User.objects.all().filter(username=username)
    if len(users) != 1:
        await send_reply_connection(websocket, False, "User not found")
        return None

    user = users[0]

    password_check = connectionPassword.objects.all().filter(idUser=user.idUser)
    if len(password_check) == 0:
        await send_reply_connection(websocket, False, "User hasn t connection password")
        return None

    hash_password = hashlib.sha512(password.encode(), usedforsecurity=True)

    if hash_password != password_check[0].password:
        await send_reply_connection(websocket, False, "Password incorrect")
        return None

    await send_reply_connection(websocket, True)
    return user.idUser
