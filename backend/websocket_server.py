import asyncio
import websockets
import datetime
import json, jwt, sys
from backend.settings import SECRET_KEY
from db_test.models import User, Message

# Liste pour stocker les connexions actives
connected_clients = set()

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
    # Add new connection
    connected_clients.add(websocket)

    try:
        # Votre logique de gestion de la connexion WebSocket
        async for data in websocket:
            print("DATA RECIEVED :", data, file=sys.stderr)
            try:
                data = json.loads(data)
                user = get_sender(data)
                if user == None:
                    continue
                print("MSG -", user.username, " :", data["message"], file=sys.stderr)

                idMsg = len(Message.objects.all())
                date = datetime.datetime.now()
                msg = Message.objects.create(id=idMsg, idUser=user, date=date, data=data["message"])
                msg.save()

            except Exception as error:
                print("CRITICAL ERROR :", error, file=sys.stderr)

    finally:
        # Supprimer la connexion lorsque le client se déconnecte
        connected_clients.remove(websocket)

# Démarrer le serveur WebSocket
start_server = websockets.serve(handle_client, "0.0.0.0", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
