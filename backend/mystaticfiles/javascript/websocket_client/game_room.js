let invite_list = [];
let popup = null;

function createGameRoom()
{
	console.log("CREATE GAME ROOM REQUEST");
	webSocket.send(JSON.stringify({
		'type' : 'gameRoom',
		'cmd' : 'createRoom'
	}));

	createListInvite();
}


function joinGameRoom(game_room_id)
{
	console.log("JOIN GAME ROOM REQUEST");
	webSocket.send(JSON.stringify({
		'type' : 'gameRoom',
		'cmd' : 'joinRoom',
		'gameRoomId' : game_room_id
	}));
}


function quitGameRoom()
{
	console.log("QUIT GAME ROOM REQUEST");
	webSocket.send(JSON.stringify({
		'type' : 'gameRoom',
		'cmd' : 'quitGameRoom'
	}));
}


function gameRoomSendInvite(user_id)
{
	console.log("SEND INVITE GAME ROOM TO USER", user_id);
	webSocket.send(JSON.stringify({
		'type' : 'gameRoom',
		'cmd' : 'inviteGameRoom',
		'targetId' : user_id
	}));
}


function gameRoomQuickUser(user_id)
{
	console.log("QUICK USER", user_id, "FROM GAME ROOM REQUEST");
	webSocket.send(JSON.stringify({
		'type' : 'gameRoom',
		'cmd' : 'quickUser',
		'targetId' : user_id
	}));
}


function gameRoomAddBot(team)
{
	console.log("ADD BOT TO TEAM ", team, " REQUEST");
	webSocket.send(JSON.stringify({
		'type' : 'gameRoom',
		'cmd' : 'addBot',
		'team' : team
	}));
}


function gameRoomRemoveBot(team)
{
	console.log("REMOVE BOT TO TEAM ", team, " REQUEST");
	webSocket.send(JSON.stringify({
		'type' : 'gameRoom',
		'cmd' : 'removeBot',
		'team' : team
	}));
}


function gameRoomChangeTeam(team)
{
	console.log("CHANGE TO TEAM ", team, " REQUEST");
	webSocket.send(JSON.stringify({
		'type' : 'gameRoom',
		'cmd' : 'changeTeam',
		'team' : team
	}));

}


function gameRoomSwitchPowerUp()
{
	console.log("SWITCH POWER UP REQUEST");
	webSocket.send(JSON.stringify({
		'type' : 'gameRoom',
		'cmd' : 'changePowerUp'
	}));
}


function gameRoomChangeMap(map_id)
{
	console.log("CHANGE MAP REQUEST");
	webSocket.send(JSON.stringify({
		'type' : 'gameRoom',
		'cmd' : 'changeMap',
		'mapId' : map_id
	}));
}


function gameRoomStartGame()
{
	console.log("START GAME REQUEST");
	webSocket.send(JSON.stringify({
		'type' : 'gameRoom',
		'cmd' : 'startGame',
	}));
}


function addUserToElement(user_id, element)
{
	let data = new FormData();
	data.append("userId", user_id);

	fetch("/getUserViewById",
		{
			method: 'POST',
			body: data,
			cache: "default"
		})
		.then(response => response.json())
		.then(jsonData => {

			if (jsonData["success"] != true)
			{
				console.log("ERROR :", jsonData["error"]);
				console.log("user id", user_id);
				return ;
			}
			let pp = document.createElement("img");
			pp.src = jsonData["pp"];
			pp.style.width = "2em";
			pp.style.height = "2em";

			let username = document.createElement("p");
			username.textContent = jsonData["username"];
			username.style.color = "white";

			let div = document.createElement("div");
			div.style.display = "flex";
			div.style.flexDirection = "row";
			div.style.backgroundColor = "rgba(18, 16, 11, 0.8)";
			div.appendChild(pp);
			div.appendChild(username);
			if (current_page == 5)
			{
				div.style.animation = "animate 0.40s infinite";
				div.onclick = function (){
					gameRoomQuickUser(user_id);
				}
			}

			element.appendChild(div);
		})
		.catch(error => console.log("get user view error :", error))
}


function addBotToElement(element, team)
{
	let pp = document.createElement("img");
	pp.src = "/static/images/default/Bosco.png";
	pp.style.width = "2em";
	pp.style.height = "2em";

	let username = document.createElement("p");
	username.textContent = "bosco";
	username.style.color = "white";

	let div = document.createElement("div");
	div.style.display = "flex";
	div.style.flexDirection = "row";
	div.style.backgroundColor = "rgba(18, 16, 11, 0.8)";
	div.appendChild(pp);
	div.appendChild(username);
	if (current_page == 5)
	{
		div.style.animation = "animate 0.40s infinite";
		div.onclick = function (){
			gameRoomRemoveBot(team);
		}
	}

	element.appendChild(div);
}


function updateGameRoomInfo(map_id, map_name, power_up, team_left, team_right)
{
	let map_name_element = document.getElementById("gameCreateMapName");
	let power_up_element = document.getElementById("gameCreatePowerStatus");
	let power_up_change_element = document.getElementById("btnStatusPowerUp");
	let team_left_element = document.getElementById("team1Player");
	let team_right_element = document.getElementById("team2Player");

	// Hilight the map choose
	for (let i = 0; i < 5; i++)
	{
		let mapBtn = document.getElementById("btnMap" + i);

		if (i == map_id)
			mapBtn.classList = "btn-drg btn-map";
		else
			mapBtn.classList = "btn-drg-dark btn-map";
	}

	if (map_name_element)
		map_name_element.textContent = map_name;

	if (power_up == "true")
	{
		if (power_up_element)
		{
			power_up_element.textContent = "ON";
			power_up_element.style.color = "green";
		}
		if (power_up_change_element)
			power_up_change_element.textContent = "ON";
	}
	else
	{
		if (power_up_element)
		{
			power_up_element.textContent = "OFF";
			power_up_element.style.color = "red";
		}
		if (power_up_change_element)
			power_up_change_element.textContent = "OFF";
	}

	// Fill left team
	if (team_left_element)
	{
		team_left_element.innerHTML = "";
		for (let i = 0; i < team_left.length; i++)
		{
			let user_id = team_left[i];

			if (user_id == -1)
				addBotToElement(team_left_element, "left");
			else
				addUserToElement(user_id, team_left_element);
		}
	}

	// Fill right team
	if (team_right_element)
	{
		team_right_element.innerHTML = "";
		for (let i = 0; i < team_right.length; i++)
		{
			let user_id = team_right[i];

			if (user_id == -1)
				addBotToElement(team_right_element, "right");
			else
				addUserToElement(user_id, team_right_element);
		}
	}
}


function createInviteContact(invite_list_container, invite_user)
{
	console.log("invite_user :", invite_user)

	let pp = document.createElement("img");
	pp.src = invite_user["pp"];
	pp.style.width = "3em";
	pp.style.height = "3em";

	let username = document.createElement("p");
	username.textContent = invite_user["name"];
	username.style.color = "white";
	username.style.width = "8em";
	username.style.margin = "0.7em";


	let div = document.createElement("div");
	div.style.display = "flex";
	div.style.flexDirection = "row";
	div.style.backgroundColor = "rgba(18, 16, 11, 0.8)";
	div.style.animation = "animate 0.40s infinite";
	div.appendChild(pp);
	div.appendChild(username);
	div.onclick = function (){
		gameRoomSendInvite(invite_user['id']);
	}

	invite_list_container.appendChild(div);
}


function createListInvite()
{
	if (popOpened)
		return ;

	fetch("/getcanbeinvited",
	{
		method: 'POST',
		cache: "default"
	})
		.then(response => response.json())
		.then (jsonData => {
			console.log("received from getcanbeinvited : ")
			console.log(jsonData)
			if (! jsonData["success"])
			{
				console.error(jsonData["content"])
				return ;
			}

			let list_invite = jsonData["listcontact"];
			let invite_list_container = document.getElementById(
											"invite_list_container");

			if (!invite_list_container)
				return ;

			invite_list_container.innerHTML = "";
			for (let i = 0; i < list_invite.length; i++)
			{
				createInviteContact(invite_list_container, list_invite[i]);
			}
		})
		.catch(error => {
			console.log("erreur from getcanbeinvited :", error)
		});
}


function deleteInvitePopup()
{
	if (popup == null)
		return ;

	popup.remove();
	if (invite_list.length == 0)
	{
		popup = null;
		return ;
	}

	let newInfo = invite_list.shift();
	createInvitePopup(newInfo[0], newInfo[1], newInfo[2]);
}


function createInvitePopup(pp_data, username_data, roomId)
{
	// Create user field
	let pp = document.createElement("img");
	pp.src = "/static/" + pp_data;
	pp.style.width = "3em";
	pp.style.height = "3em";

	let username = document.createElement("p");
	username.textContent = username_data;
	username.style.color = "white";
	username.style.width = "8em";
	username.style.margin = "0.7em";

	let userField = document.createElement("div");
	userField.style.display = "flex";
	userField.style.flexDirection = "row";
	userField.appendChild(pp);
	userField.appendChild(username);

	// Create text
	let text = document.createElement("p");
	text.textContent = "Invited you to play a game of pong at the abyss bar !";
	text.style.color = "white";
	text.style.width = "100%";
	text.style.textAlign = "center";

	// Create reply buttons
	let accept = document.createElement("button");
	accept.textContent = "Accept";
	accept.classList = "btn-drg";
	accept.style.marginLeft = "20%";
	accept.onclick = function () {
		joinGameRoom(roomId);
		deleteInvitePopup();
	}

	let refuse = document.createElement("button");
	refuse.textContent = "Refuse";
	refuse.classList = "btn-drg";
	refuse.style.marginLeft = "20%";
	refuse.onclick = function () {
		deleteInvitePopup();
	}

	let butDiv = document.createElement("div");
	butDiv.style.display = "flex";
	butDiv.style.flexDirection = "row";
	butDiv.style.marginBottom = "2%";
	butDiv.appendChild(accept);
	butDiv.appendChild(refuse);

	// Body of popup
	popup = document.createElement("div");
	popup.style.width = "15em";
	popup.style.display = "absolute";
	popup.style.textAlign = "center";
	popup.style.top = "20em";
	popup.style.left = "4em";
	popup.style.backgroundColor = "rgba(18, 16, 11, 0.9)" ;
	popup.style.borderRadius= "30px";
	popup.style.border= "solid #ff9c00";
	popup.style.marginTop= "1%";
	popup.style.marginLeft= "1%";
	popup.appendChild(userField);
	popup.appendChild(text);
	popup.appendChild(butDiv);

	console.log("Create Popup !");
	document.body.appendChild(popup);
}
