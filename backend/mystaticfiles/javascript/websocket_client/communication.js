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
		if (current_page == 5 || current_page == 8)
			alert(data['error']);
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

		const mapId = data["mapId"];
		const mapName = data["mapName"];
		const power_up = data["powerUpActivate"];
		const team_left = data["teamLeft"];
		const team_right = data["teamRight"];
		updateGameRoomInfo(mapId, mapName, power_up, team_left, team_right);
	}
	else if (type == 'joinRoomInfo')
	{
		console.log("GAME ROOM JOINED");
		if (current_page != 51)
			changePage('51');

		let inter = setInterval(function () {
			if (pageInLoad == false)
			{
				const mapId = data["mapId"];
				const mapName = data["mapName"];
				const power_up = data["powerUpActivate"];
				const team_left = data["teamLeft"];
				const team_right = data["teamRight"];
				updateGameRoomInfo(mapId, mapName, power_up, team_left, team_right);
				clearInterval(inter);
			}
			else
				console.log("wait");
		}, 10);
	}
	else if (type == 'updateRoomInfo')
	{
		console.log("GAME ROOM UPDATE");

		const mapId = data["mapId"];
		const mapName = data["mapName"];
		const power_up = data["powerUpActivate"];
		const team_left = data["teamLeft"];
		const team_right = data["teamRight"];
		updateGameRoomInfo(mapId, mapName, power_up, team_left, team_right);
	}
	else if (type == 'invite')
	{
		if (current_page != 3 && current_page != 4 && current_page != 5 && current_page != 14)
			return ;
		const pp = data["pp"];
		const username = data["username"];
		const roomId = data["roomId"];
		if (popup == null)
			createInvitePopup(pp, username, roomId);
		else
			invite_list.push([pp, username, roomId])
	}
	else if (type == 'quitGameRoom')
	{
		console.log("QUIT GAME ROOM");
		if (current_page == 5 || current_page == 51)
			changePage('3');
	}
	else if (type == 'quickFromGameRoom')
	{
		console.log("QUICK FROM GAME ROOM");
		if (current_page == 5 || current_page == 51)
			changePage('3');
	}
	else if (type == 'gameStart')
	{
		console.log("GAME START !");
		let port = data["gamePort"];
		let id_paddle = data["paddleId"];
		let id_team = data["teamId"];
		let get_game_type = data["gameType"];
		startGameClient(port, id_paddle, id_team, get_game_type);
	}
	else if (type == 'tournamentState')
	{
		console.log("tournament state", current_page);
		let status = data["status"];
		let mapId = data["mapId"];
		let mapName = data["mapName"];
		let powerUp = data["powerUp"];
		let listPlayers = data["players"];
		let youInTournament = data["youAreInTournament"];
		console.log("MSG RECIVIED ON PAGE", current_page);
		if (pageForTournamentStatus == "mainpage" || current_page == 3)
			manageMainpageButton(status, mapName, powerUp, listPlayers, youInTournament);
		else if (pageForTournamentStatus == "create" || current_page == 8)
			assignTournamentStatusOnCreatePage(status, mapId, powerUp, listPlayers);
		else if (current_page == 71 || current_page == 72)
			applyTournamentState(status, mapName, powerUp, listPlayers, youInTournament);
		pageForTournamentStatus = null;
	}
	else if (type == 'joinReply')
	{
		console.log("Tournament join succeed");

		let powerUp = data["powerUp"];
		let mapName = data["mapName"];
		let players = data["players"];

		changePage('71');
		waitTournamentState(1, mapName, powerUp, players, 'true');
	}
	else if (type == 'quitReply')
	{
		console.log("Tournament quit succeed");
		changePage('3');
	}
	else if (type == 'tournamentTreeUpdate')
	{
		let playersGrade = data['playersGrade'];
		waitTournamentTree(playersGrade)
	}
	else if (type == 'nextMatch')
	{
		let match = data['match'];
		waitTournamentNextMatch(match);
	}
	else if (type == 'myNextMatch')
	{
		let match = data['match'];
		waitTournamentMyNextMatch(match);
	}
	else if (type == 'tournamentStart')
	{
		let powerUp = data["powerUp"];
		let mapId = data["mapId"];
		let mapName = data["mapName"];
		let listPlayers = data["players"];
		let youInTournament = data["inTournament"];
		if (current_page == 3)
			manageMainpageButton(2, mapName, powerUp, listPlayers, youInTournament);
		else if (current_page == 8)
			assignTournamentStatusOnCreatePage(2, mapId, powerUp, listPlayers);
		else if (current_page == 71 || current_page == 72)
			applyTournamentState(2, mapName, powerUp, listPlayers, youInTournament);
	}
	else if (type == 'winners')
	{
		let winner = data['onePongMan'];
		let second = data['second'];
		let third = data['third'];
		waitTournamentResult(winner, second, third);
	}
	else if (type == 'endTournament')
	{
		if (current_page == 70 || current_page == 71 || current_page == 72)
		{
			changePage('73');
			let winner = data['onePongMan'];
			let second = data['second'];
			let third = data['third'];
			waitTournamentResult(winner, second, third);
		}
		else if (current_page == 3)
		{
			manageMainpageButton(3, 0, "false", [], "false");
		}
		else if (current_page == 8)
		{
			assignTournamentStatusOnCreatePage(3, 0, "false", []);
		}

	}
	else if (type == 'winnersTournament')
	{
		let winner = data['onePongMan'];
		let second = data['second'];
		let third = data['third'];
		waitTournamentResult(winner, second, third);
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
