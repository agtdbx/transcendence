


let ws_game = null;
let id_paddle = null;
let id_team = null;
let game_type = null

let keydownListennerGame = null;
let keyupListennerGame = null;


function startGameClient(server_port, idPaddle, idTeam, get_game_type)
{
	if (ws_game != null)
		return ;
	console.log("Try create game webSocket at wss://" + window.location.hostname + ":" + server_port + "/");
	try {
		ws_game = new WebSocket("wss://" + window.location.hostname + ":" + server_port + "/")
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
		game_type = get_game_type;
	}

	ws_game.onerror = function(e) {console.error("GWS ERROR :", e)};
	websockGame = ws_game;
}

function startGameLocalClient(server_port, idPaddle, idTeam, get_game_type)
{
	if (ws_game != null)
		return ;
	console.log("Try create game webSocket at wss://" + window.location.hostname + ":" + server_port + "/");
	try {
		ws_game = new WebSocket("wss://" + window.location.hostname + ":" + server_port + "/")
	}
	catch (error)
	{
		console.error("GWS GAME ERROR :", error);
		return
	}
	paddleInfoUser = [parseInt(idPaddle), parseInt(idTeam)];

	ws_game.onopen = function(e)
	{
		console.log("Client gws local connection ok !");
		// Go to game page
		changePage('6');
		gameStartLocal = true;
		ws_game.send(JSON.stringify({
			'type' : 'userIdentification'
		}));
		game_type = get_game_type;
	}

	ws_game.onerror = function(e) {console.error("GWS ERROR :", e)};
	websockGame = ws_game;
}
