


let ws_game = null;
let id_paddle = null;
let id_team = null;

function startGameClient(server_port, idPaddle, idTeam)
{
	if (ws_game != null)
		return ;
	console.log("Try create game webSocket at ws://" + window.location.hostname + ":" + server_port + "/");
	try {
		ws_game = new WebSocket("ws://" + window.location.hostname + ":" + server_port + "/")
	}
	catch (error)
	{
		console.error("GWS GAME ERROR :", error);
		return
	}
	paddleInfoUser = [parseInt(idPaddle), parseInt(idTeam)];

	ws_game.onopen = function(e)
	{
		console.log("Client gws connection ok !");
		// Go to game page
		changePage('6');
		gameStart = true;
		ws_game.send(JSON.stringify({
			'type' : 'userIdentification',
			'idPaddle' : idPaddle,
			'idTeam': idTeam
		}));
	}

	ws_game.onerror = function(e) {console.error("GWS ERROR :", e)};
	websockGame = ws_game;
}


// function parseServerMessage(event)
// {
// 	let data = null;
// 	try
// 	{
// 		data = JSON.parse(event.data);
// 		console.log("DATA FROM GWS :", data);
// 	}
// 	catch (error)
// 	{
// 		console.error("GWS : Json parsing error :", event.data, error);
// 		return ;
// 	}

// 	const type = data['type'];

// 	if (type === "error")
// 	{
// 		console.error("GWS :Error :", data['error']);
// 	}
// 	else if (type === "endGame") // Not the movie !
// 	{
// 		let but = document.createElement("button");
// 		but.classList = "btn-drg";
// 		but.textContent = "Return to main page";
// 		but.onclick = function(){
// 			changePage('3');
// 		};
// 		document.getElementById("content").appendChild(but);
// 		ws_game.onclose = {};
// 		ws_game.close();
// 		ws_game = null;
// 		id_paddle = null;
// 		id_team = null;
// 		console.log("GWS CLOSE");
// 	}
// 	else
// 		console.error("GWS :Unkown data recieved :", data);
// }
