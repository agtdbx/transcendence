import sys
import datetime
from db_test.models import User, Message, PrivMessage


async def general_message(message:str, user:User, connected_clients:dict):
    idMsg = len(Message.objects.all())
    date = datetime.datetime.now()
    msg = Message.objects.create(id=idMsg, idUser=user, date=date, data=message)
    msg.save()

    message = message.replace("'", " ")
    message = message.replace('"', '')
    strMessage = str({"message" : message, "username" : user.username, "pp" : "/media/" + str(user.profilPicture),
                    "date" : str(date), "channel" : "general"})
    strMessage = strMessage.replace("'", '"')

    print("client states :", connected_clients, file=sys.stderr)
    for _, websockets in connected_clients.items():
        toDelete = []
        for i in range(len(websockets)):
            websocket = websockets[i]
            print("MSG SEND", file=sys.stderr)
            try:
                await websocket.send(strMessage)
            except:
                toDelete.append(i)
                print("MSG SEND FAIL", file=sys.stderr)
        for i in range(len(toDelete)):
            websockets.pop(toDelete[i] - i)
            if len(websockets) == 0:
                user = User.objects.all().filter(idUser=id)[0]
                user.idStatus = 0
                user.save()


async def private_message(myid:int, channel:str, message:str, user:User, connected_clients:dict):
    try:
        idTarget = int(channel)
        testTarget = User.objects.all().filter(idUser=idTarget)
        if len(testTarget) != 1:
            print("TARGET NOT FOUND :", idTarget, file=sys.stderr)
            return

        idMsg = len(PrivMessage.objects.all())
        date = datetime.datetime.now()
        msg = PrivMessage.objects.create(id=idMsg, idUser=user, date=date, data=message, idTarget=idTarget)
        msg.save()

        pp = "/media/" + str(user.profilPicture)

        message = message.replace("'", " ")
        message = message.replace('"', '')
        strMessage = str({"message" : message, "username" : user.username, "pp" : pp,
                        "date" : str(date), "channel" : str(idTarget)})
        strMessageTarget = str({"message" : message, "username" : user.username, "pp" : pp,
                        "date" : str(date), "channel" : str(myid)})
        strMessage = strMessage.replace("'", '"')
        strMessageTarget = strMessageTarget.replace("'", '"')

        print("client states :", connected_clients, file=sys.stderr)
        for id, websockets in connected_clients.items():
                if id == user.idUser:
                    toDelete = []
                    for i in range(len(websockets)):
                        websocket = websockets[i]
                        try:
                            await websocket.send(strMessage)
                        except:
                            toDelete.append(i)
                            print("MSG SEND FAIL", file=sys.stderr)
                    for i in range(len(toDelete)):
                        websockets.pop(toDelete[i] - i)
                        if len(websockets) == 0:
                            user = User.objects.all().filter(idUser=id)[0]
                            user.idStatus = 0
                            user.save()
                elif id == idTarget:
                    toDelete = []
                    for i in range(len(websockets)):
                        websocket = websockets[i]
                        try:
                            await websocket.send(strMessageTarget)
                        except:
                            toDelete.append(i)
                            print("MSG SEND FAIL", file=sys.stderr)
                    for i in range(len(toDelete)):
                        websockets.pop(toDelete[i] - i)
                        if len(websockets) == 0:
                            user = User.objects.all().filter(idUser=id)[0]
                            user.idStatus = 0
                            user.save()

    except Exception as error:
        print("CHANNEL CAN'T BE PARSE TO INT :", channel, "\nerror :", error, file=sys.stderr)
