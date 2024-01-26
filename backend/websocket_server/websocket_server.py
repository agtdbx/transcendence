import asyncio
import websockets
import json, jwt, sys, os
from backend.settings import SECRET_KEY
from db_test.models import User
from websocket_server.chat.message import general_message, private_message
import ssl

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
try :
    # ssl_cert = "/certs/certificate.crt"
    # ssl_key = "/certs/private.key"
    ssl_cert = "/certs/server.crt"
    ssl_key = "/certs/server.pem"

    ssl_context.load_cert_chain(ssl_cert, keyfile=ssl_key)
except Exception as error:
    print("ERROR ON LOAD SSH CERT AND KEY :", error, file=sys.stderr)
    exit()

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
                    user = User.objects.all().filter(idUser=myid)[0]
                    user.idStatus = 1
                    user.save()
                continue

            user = get_sender(data)
            channel = data.get("channel", None)
            message = data.get("message", None)

            if user == None or channel == None or message == None:
                print("BAD DATA RECIEVED", file=sys.stderr)
                continue

            print(user.username, user.profilPicture, ":", data["message"], file=sys.stderr)
            if channel == "general":
                await general_message(message, user, connected_clients)
                continue
            await private_message(myid, channel, message, user, connected_clients)

    except Exception as error:
        print("CRITICAL ERROR :", error, file=sys.stderr)

    finally:
        # Supprimer la connexion lorsque le client se déconnecte
        if myid != None:
            print("Bye bye client " + str(myid) + " :", connected_clients, file=sys.stderr)
            connected_clients.get(myid, []).remove(websocket)
            print("After delete client " + str(myid) + " :", connected_clients, file=sys.stderr)
            if len(connected_clients.get(myid, [])) == 0:
                user = User.objects.all().filter(idUser=myid)[0]
                user.idStatus = 0
                user.save()


# Démarrer le serveur WebSocket
start_server = websockets.serve(handle_client, "0.0.0.0", 8765, ssl=ssl_context)
# start_server = websockets.serve(handle_client, "0.0.0.0", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
