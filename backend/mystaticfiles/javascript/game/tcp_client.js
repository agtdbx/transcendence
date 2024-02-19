import "./define.js"
import  {GameClient} from "./game_client.js"

// import select
// import socket

var actuelGame = null;

const sleep = ms => new Promise(r => setTimeout(r, ms));



function parseMessageFromServerWS(event)
{
	// try
	// {
		actuelGame.parseMessageFromServer(event);
	// }
	// catch (error)
	// {
	// 	console.log(console.error(error));
	// }

}

export async function runGameClient(
        host="127.0.0.1",
        port=20000
    )
{
	websockGame.onmessage = parseMessageFromServerWS;
    // Start tcp client
    // clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    // clientSocket.connect((host, port))

    // pollerObject = select.poll()
    // pollerObject.register(clientSocket, select.POLLIN)

    let isReady = false

    // Start game client
    let gameClient = new GameClient()
	actuelGame = gameClient;

	keydownListennerGame = function(event)
	{
		console.log("event detected : " + event.code)
		gameClient.input(event, "down")
	}

	keyupListennerGame = function(event)
	{
		console.log("event detected : " + event.code)
		gameClient.input(event, "up")
	}

	document.addEventListener("keydown", keydownListennerGame);
	document.addEventListener("keyup", keyupListennerGame);

    // Clients loop

		var intervalGame = setInterval(
			function ()
			{
				if (!isReady && gameClient.runMainLoop)
				{
					gameClient.step()
					isReady = true
				}
				else if (isReady && gameClient.runMainLoop)
				{
					gameClient.step()
					//console.log("game step")
				}
				else if (isReady)
				{
					console.log("game end")
					gameClient.quit()
					clearInterval(interval);
				}
			},
			16); //value : 16

}

