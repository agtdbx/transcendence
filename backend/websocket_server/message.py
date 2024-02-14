import asyncio
import sys
import datetime
from websocket_server.utils import send_error, get_user_by_id, get_user_by_username
from websocket_server.game_room import send_game_room_invite
from db_test.models import User, Message, PrivMessage, Link


def create_str_message(message, username, pp, date, channel):
    message = message.replace("'", " ")
    message = message.replace('"', '')

    str_message = str({"type" : "message",
                       "message" : message,
                       "username" : username,
                       "pp" : pp,
                       "date" : str(date),
                       "channel" : str(channel)})
    str_message = str_message.replace("'", '"')

    return str_message

def isBlocked(user_id:int, user:User):
    linkFriendRequestList = Link.objects.all().filter(idUser=user_id, idTarget=user.idUser)
    if (len(linkFriendRequestList) < 1):
        return False
    return (linkFriendRequestList[0].link == 3)
    # blockedUsers = []
    # for link in linkFriendRequestList :
    #     try:
    #         friend = User.objects.all().filter(idUser=link.idTarget)[0]
    #         blockedUsers.append(friend.idUser)
    #     except:
    #         continue
    # for user.idUser in blockedUsers:
    #     return True
    # return False

async def message_in_general(message:str, user:User, connected_users:dict):
    id_msg = Message.objects.count()
    date = datetime.datetime.now()
    msg = Message.objects.create(id=id_msg, idUser=user, date=date, data=message)
    msg.save()

    str_message = create_str_message(message, user.username,
                                     "/static/" + str(user.profilPicture),
                                     date, "general")

    print("\nclient states :", connected_users, file=sys.stderr)
    for user_id, websockets in connected_users.items():
        for i in range(len(websockets)):
            if isBlocked(user_id, user) == False:
                websocket = websockets[i]
            try:
                await websocket.send(str_message)
                print("MSG SEND", file=sys.stderr)
            except:
                print("MSG SEND FAIL", file=sys.stderr)


async def message_in_private(message:str,
                             myid:int,
                             user:User,
                             target_id:int,
                             connected_users:dict):
    id_msg = PrivMessage.objects.count()
    date = datetime.datetime.now()
    msg = PrivMessage.objects.create(id=id_msg, idUser=user, date=date,
                                     data=message, idTarget=target_id)
    msg.save()

    pp = "/static/" + str(user.profilPicture)
    str_msg_to_target = create_str_message(message, user.username, pp, date, myid)
    str_msg_to_myuser = create_str_message(message, user.username, pp, date,
                                           target_id)

    # Send message to user
    print("\nSEND MSG TO USER :", myid, file=sys.stderr)
    for websocket in connected_users.get(myid, []):
        try:
            await websocket.send(str_msg_to_myuser)
            print("SEND OK", file=sys.stderr)
        except:
            print("SEND FAIL", file=sys.stderr)

    # Send message to target
    print("\nSEND MSG TO TARGET :", target_id, file=sys.stderr)
    for websocket in connected_users.get(target_id, []):
        try:
            await websocket.send(str_msg_to_target)
            print("SEND OK", file=sys.stderr)
        except:
            print("SEND FAIL", file=sys.stderr)


async def recieved_message(data : dict,
                           connected_users : dict,
                           websocket,
                           myid : int,
                           game_room_id:int,
                           game_rooms:dict):
    message : str = data.get("message", None)
    channel = data.get("channel", None)

    if message == None or channel == None:
        await send_error(websocket, "Message or channel field missing")
        return

    user : User = get_user_by_id(myid)
    if user == None:
        await send_error(websocket, "Error when get user")
        return
    
    if message[0:8] == "/invite ":
        print("\nWS : /invite detected", file=sys.stderr)
        username = message[8:]
        username = username.lower()
        print("WS : username :", username, file=sys.stderr)
        # check if username exist
        userTarget = get_user_by_username(username)
        if userTarget != None:
            print("WS : username ok, send invite", file=sys.stderr)
            # appeller invite de gameroom
            data = {"targetId" : userTarget.idUser}
            await send_game_room_invite(myid, connected_users, data,
                                        game_room_id, game_rooms)
        return

    if channel == "general":
        await message_in_general(message, user, connected_users)
        return

    try:
        target_id = int(channel)
        target = get_user_by_id(target_id)

        if target == None:
            await send_error(websocket, "Invalid private channel")
            return

        await message_in_private(message, myid, user, target_id, connected_users)

    except Exception as error:
        await send_error(websocket, "Invalid channel")
        print("\nChannel :", channel, "ERROR :", error, file=sys.stderr)
