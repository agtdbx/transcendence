import "./define.js"
import  /*{GameClient} from*/ "./game_client.js"

// import select
// import socket

function runGameClient(
        host="127.0.0.1",
        port=20000
    )
{
    // Start tcp client
    // clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    // clientSocket.connect((host, port))

    // pollerObject = select.poll()
    // pollerObject.register(clientSocket, select.POLLIN)

    runTcpClient = true

    // Start game client
    gameClient = GameClient()

    // Clients loop
    while(runTcpClient && gameClient.runMainLoop)
	{
        // Check if we recived message
        //fdVsEvent = pollerObject.poll(10)

        // Parse the messages recieved
        // for (const pair of fdVsEvent)
		// {
		// 	const descriptor = pair[0];
		// 	const Event = pair[1];
        //     if (descriptor == clientSocket.fileno())
		// 	{
        //         msg = clientSocket.recv(65536).decode('utf-8')
        //         if (! msg)
		// 		{
        //             print("Server close")
        //             runTcpClient = False
        //             break
		// 		}
        //         messages = msg.split("|")
        //         for (const message of messages)
		// 		{
        //             try
		// 			{
        //                 srv_msg = eval(message)
        //                 gameClient.messageFromServer.append(srv_msg)
		// 			}
        //             catch
		// 			{
        //                 console.log(message)
        //                 pass
		// 			}
		// 		}
		// 	}
		// }

        // Run game client step
        gameClient.step()

        // Send the server state to client
        // for (const msg of gameClient.messageForServer)
        //     clientSocket.sendall(bytes(str(msg) + "|", encoding='utf-8'))
	}
    // if (gameClient.runMainLoop == false)
    //     clientSocket.sendall(bytes(str("STOP"), encoding='utf-8'))

    print("Client_end")
    gameClient.quit()
}

