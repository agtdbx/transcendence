from define import *
from server_side.game_server import GameServer

import select
import socket


TIME_OUT = 60000


def runGameServer(
        ipAddress:str="127.0.0.1",
        port:int=20000,
        map_to_load:int=0,
        paddles_left:list[int]=[PADDLE_PLAYER],
        paddles_right:list[int]=[PADDLE_IA],
        powerUpEnable:bool=False
    ):
    # Start tcp server
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    serverSocket.bind((ipAddress, port))
    serverSocket.listen()

    pollerObject = select.poll()
    pollerObject.register(serverSocket, select.POLLIN)

    clientSockets = []
    numberOfSockets = 0

    runTcpServer = True
    timeBeforeTimeout = TIME_OUT

    # Start game server
    gameServer = GameServer(powerUpEnable, paddles_left, paddles_right, map_to_load)
    gameConfingMsgs = gameServer.messageForClients.copy()

    # Servers loop
    while(runTcpServer and gameServer.runMainLoop):
        # Check if we recived message
        fdVsEvent = pollerObject.poll(10)

        if len(fdVsEvent) == 0:
            timeBeforeTimeout -= 10
            if timeBeforeTimeout <= 0:
                runTcpServer = False
                print("TIMEOUT")
                break
        else:
            timeBeforeTimeout = TIME_OUT

        # Parse the messages recieved
        socketToRemove = []
        for descriptor, Event in fdVsEvent:
            if descriptor == serverSocket.fileno():
                conn, addr = serverSocket.accept()
                print("Client", len(clientSockets), "added")
                pollerObject.register(conn, select.POLLIN)
                clientSockets.append(conn)
                numberOfSockets += 1
                # Send the game config to the client
                for gameConfingMsg in gameConfingMsgs:
                    conn.sendall(bytes(str(gameConfingMsg) + "|", encoding='utf-8'))
                continue
            for i in range(len(clientSockets)):
                if descriptor == clientSockets[i].fileno():
                    try:
                        msg = clientSockets[i].recv(65536).decode('utf-8')
                        if not msg:
                            socketToRemove.append(i)

                        elif msg == "STOP":
                            runTcpServer = False
                        else:
                            # In we have a message, we send it to
                            messages = msg.split("|")
                            for message in messages:
                                try:
                                    cli_msg = eval(message)
                                    gameServer.messageFromClients.append(cli_msg)
                                except:
                                    pass
                    except:
                        socketToRemove.append(i)

        for i in range(len(socketToRemove)):
            print("Client", i, "disconnected")
            pollerObject.unregister(clientSockets[i])
            clientSockets.pop(socketToRemove[i] - i)

        # Run game server step
        if numberOfSockets >= 1:
            gameServer.step()

            # Send the server state to client
            for msg in gameServer.messageForClients:
                for clientSocket in clientSockets:
                    try:
                        clientSocket.sendall(bytes(str(msg) + "|", encoding='utf-8'))
                    except:
                        pass

    print("Server_end")
    gameServer.printFinalStat()
