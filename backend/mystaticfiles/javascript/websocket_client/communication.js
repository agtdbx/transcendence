function onRecieveData(event)
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
	else if (type == 'connectionReply')
	{
		if (data['success'] == false)
			console.error("Connection failed :", data['error']);
		else
			console.log("Connection OK");
	}
	else if (type == 'message')
	{
		recievedMessage(data);
	}
	else if (type == 'joinWaitlist')
	{
		if (current_page != 4)
			changePage('4');
	}
	else if (type == 'quitWaitlist')
	{
		if (current_page != 3)
			changePage('3');
	}
	else if (type == 'createRoomInfo')
	{
		console.log("GAME ROOM CREATED");
		if (current_page != 5)
			changePage('5');

		const map_id = data["mapId"];
		const power_up = data["powerUpActivate"];
		const team_left = data["teamLeft"];
		const team_right = data["teamRight"];
		updateGameRoomInfo(map_id, power_up, team_left, team_right);
	}
	else if (type == 'joinRoomInfo')
	{
		console.log("GAME ROOM JOINED");
		if (current_page != 5)
			changePage('5');

		const map_id = data["mapId"];
		const power_up = data["powerUpActivate"];
		const team_left = data["teamLeft"];
		const team_right = data["teamRight"];
		updateGameRoomInfo(map_id, power_up, team_left, team_right);
	}
	else if (type == 'updateRoomInfo')
	{
		console.log("GAME ROOM UPDATE");

		const map_id = data["mapId"];
		const power_up = data["powerUpActivate"];
		const team_left = data["teamLeft"];
		const team_right = data["teamRight"];
		updateGameRoomInfo(map_id, power_up, team_left, team_right);
	}
	else if (type == 'quitGameRoom')
	{
		console.log("QUIT GAME ROOM");
		if (current_page == 5)
			changePage('3');
	}
	else if (type == 'gameStart')
	{
		console.log("GAME START !");
		let port = data["gamePort"];
		let id_paddle = data["paddleId"];
		let id_team = data["teamId"];
		startGameClient(port, id_paddle, id_team);
	}
	else
		console.error("Unkown data recieved :", data);
}


function recievedMessage(data) {
	const channel = data['channel'];
	const message = data['message'];
	const username = data['username'];
	const pp = data['pp'];
	const date = data['date'].substring(11, 19);
	if (channel == channelTarget)
	{
		addNewMessage(message, username, pp, date);

		if (chatScrollAtBottom)
			chatElement.scrollTop = chatElement.scrollHeight;
	}
}


// Send message to server
function sendMessageToServer(message, channel) {
	webSocket.send(JSON.stringify({
		'type' : 'message',
		'cmd' : 'sendMessage',
		'message': message,
		'channel' : channel
	}));
}


function sendMessage(input)
{
	if (input.value == "")
		return ;
	chatScrollAtBottom = true;
	sendMessageToServer(input.value, channelTarget);
	input.value = "";
}
