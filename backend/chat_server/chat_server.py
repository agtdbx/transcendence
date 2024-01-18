import asyncio
import websockets
import datetime
import json, jwt, sys
from backend.settings import SECRET_KEY
from db_test.models import User, Message, PrivMessage

# Liste pour stocker les connexions actives
connected_clients = dict()

def get_id(data):
    token = data.get("whoiam", None)
    if token == None:
        return None

    jwtData = jwt.decode(token, SECRET_KEY, algorithms="HS256")
    if jwtData == None:
        return None

    idUser = jwtData.get("userId", None)
    if idUser == None:
        return None

    return idUser


def get_sender(data):
    token = data.get("sender", None)
    if token == None:
        return None

    jwtData = jwt.decode(token, SECRET_KEY, algorithms="HS256")
    if jwtData == None:
        return None

    idUser = jwtData.get("userId", None)
    if idUser == None:
        return None

    users = User.objects.all().filter(idUser=idUser)
    if len(users) != 1:
        return None
    return users[0]


async def handle_client(websocket, path):
    myid = None

    try:
        # Votre logique de gestion de la connexion WebSocket
        async for data in websocket:
            print("DATA RECIEVED :", data, file=sys.stderr)
            data = json.loads(data)

            if myid == None:
                myid = get_id(data)
                if myid != None:
                    sockets = connected_clients.get(myid, [])
                    sockets.append(websocket)
                    connected_clients[myid] = sockets
                    print("New client added :", connected_clients, file=sys.stderr)
                continue

            user = get_sender(data)
            channel = data.get("channel", None)
            message = data.get("message", None)


            if user == None or channel == None or message == None:
                print("BAD DATA RECIEVED", file=sys.stderr)
                continue

            print(user.username, user.profilPicture, ":", data["message"], file=sys.stderr)
            if channel == "general":
                idMsg = len(Message.objects.all())
                date = datetime.datetime.now()
                msg = Message.objects.create(id=idMsg, idUser=user, date=date, data=message)
                msg.save()

                message = message.replace("'", " ")
                message = message.replace('"', '')
                strMessage = str({"message" : message, "username" : user.username, "pp" : "./media/" + str(user.profilPicture),
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
                continue

            try:
                idTarget = int(channel)
                testTarget = User.objects.all().filter(idUser=idTarget)
                if len(testTarget) != 1:
                    print("TARGET NOT FOUND :", idTarget, file=sys.stderr)
                    continue

                idMsg = len(PrivMessage.objects.all())
                date = datetime.datetime.now()
                msg = PrivMessage.objects.create(id=idMsg, idUser=user, date=date, data=message, idTarget=idTarget)
                msg.save()

                pp = "./media/" + str(user.profilPicture)

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

            except Exception as error:
                print("CHANNEL CAN'T BE PARSE TO INT :", channel, "\nerror :", error, file=sys.stderr)


    except Exception as error:
        print("CRITICAL ERROR :", error, file=sys.stderr)

    finally:
        # Supprimer la connexion lorsque le client se déconnecte
        if myid != None:
            connected_clients.get(myid, []).remove(websocket)
            print("Bye bye client " + str(myid) + " :", connected_clients, file=sys.stderr)
# Démarrer le serveur WebSocket
start_server = websockets.serve(handle_client, "0.0.0.0", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
