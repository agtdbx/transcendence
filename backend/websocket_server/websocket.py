import asyncio
import websockets

# Liste pour stocker les connexions actives
connected_clients = set()

async def handle_client(websocket, path):
    # Ajouter la nouvelle connexion à la liste
    connected_clients.add(websocket)

    try:
        # Votre logique de gestion de la connexion WebSocket
        async for message in websocket:
            # Traitement du message reçu
            # ...
            pass

    finally:
        # Supprimer la connexion lorsque le client se déconnecte
        connected_clients.remove(websocket)

# Démarrer le serveur WebSocket
start_server = websockets.serve(handle_client, "0.0.0.0", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
