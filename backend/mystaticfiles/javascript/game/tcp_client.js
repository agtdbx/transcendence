// from define import *
// from client_side.game_client import GameClient

// import select
// import socket

def runGameClient(
        host:str="127.0.0.1",
        port:int=20000
    ):
    // Start tcp client
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((host, port))

    pollerObject = select.poll()
    pollerObject.register(clientSocket, select.POLLIN)

    runTcpClient = true

    // Start game client
    gameClient = GameClient()

    // Clients loop
    while(runTcpClient and gameClient.runMainLoop):
        // Check if we recived message
        fdVsEvent = pollerObject.poll(10)

        // Parse the messages recieved
        for descriptor, Event in fdVsEvent:
            if descriptor == clientSocket.fileno():
                msg = clientSocket.recv(65536).decode('utf-8')
                if not msg:
                    print("Server close")
                    runTcpClient = False
                    break
                messages = msg.split("|")
                for message in messages:
                    try:
                        srv_msg = eval(message)
                        gameClient.messageFromServer.append(srv_msg)
                    except:
                        print(message)
                        pass

        // Run game client step
        gameClient.step()

        // Send the server state to client
        for msg in gameClient.messageForServer:
            clientSocket.sendall(bytes(str(msg) + "|", encoding='utf-8'))

    if gameClient.runMainLoop == False:
        clientSocket.sendall(bytes(str("STOP"), encoding='utf-8'))

    print("Client_end")
    gameClient.quit()
