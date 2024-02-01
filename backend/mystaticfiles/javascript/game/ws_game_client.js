let ws_game = null;
let id_paddle = null;
let id_team = null;

function startGameClient(server_port, id_paddle, id_team)
{
	console.log("Try create game webSocket at ws://" + window.location.hostname + ":" + server_port + "/");
	try {
		ws_game = new WebSocket("ws://" + window.location.hostname + ":" + server_port + "/")
	}
	catch (error)
	{
		console.error("WS GAME ERROR :", error);
		return
	}

	ws_game.onopen = function(e)
	{
		console.log("Client ws connection ok !");
		// Go to game page
		changePage('5');
		ws_game.send(JSON.stringify({
			'type' : 'userIdentification',
			'id_paddle' : id_paddle,
			'id_team': id_team
		}));
	}

	ws_game.onmessage = parseServerMessage;

	ws_game.onerror = function(e) {console.error("WS GAME ERROR :", e)};
}


function parseServerMessage(event)
{
	let data = null;
	try
	{
		data = JSON.parse(event.data);
	}
	catch (error)
	{
		console.error("Json parsing error :", event.data, error);
		return ;
	}

	const type = data['type'];

	if (type === "error")
	{
		console.error("Error :", data['error']);
	}
	else
		console.error("Unkown data recieved :", data);
}
