import asyncio
import websockets
import datetime
import json, jwt, sys
from backend.settings import SECRET_KEY
from db_test.models import User, Message

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
    id = None

    try:
        # Votre logique de gestion de la connexion WebSocket
        async for data in websocket:
            print("DATA RECIEVED :", data, file=sys.stderr)
            data = json.loads(data)

            if id == None:
                id = get_id(data)
                if id != None:
                    sockets = connected_clients.get(id, [])
                    sockets.append(websocket)
                    connected_clients[id] = sockets
                    print("New client added :", connected_clients, file=sys.stderr)
                continue

            user = get_sender(data)
            channel = data.get("channel", None)
            message = data.get("message", None)

            if user == None or channel == None or message == None:
                print("BAD DATA RECIEVED", file=sys.stderr)
                continue

            print("MSG -", user.username, " :", data["message"], file=sys.stderr)
            if channel == "general":
                idMsg = len(Message.objects.all())
                date = datetime.datetime.now()
                msg = Message.objects.create(id=idMsg, idUser=user, date=date, data=message)
                msg.save()

                strMessage = str({"message" : message, "username" : user.username, "pp" : ""})
                strMessage = strMessage.replace("'", '"')

                for _, websockets in connected_clients.items():
                    for websocket in websockets:
                        await websocket.send(strMessage)

    except Exception as error:
        print("CRITICAL ERROR :", error, file=sys.stderr)

    finally:
        # Supprimer la connexion lorsque le client se déconnecte
        if id != None:
            connected_clients.get(id, []).remove(websocket)
            print("Bye bye client :", connected_clients, file=sys.stderr)
# Démarrer le serveur WebSocket
start_server = websockets.serve(handle_client, "0.0.0.0", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
