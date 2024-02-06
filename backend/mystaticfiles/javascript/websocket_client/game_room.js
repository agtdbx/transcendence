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

	createListInvite();
}


function quitGameRoom()
{
	console.log("QUIT GAME ROOM REQUEST");
	webSocket.send(JSON.stringify({
		'type' : 'gameRoom',
		'cmd' : 'quitGameRoom'
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


function updateGameRoomInfo(map_id, power_up, team_left, team_right)
{
	let map_name_element = document.getElementById("gameCreateMapName");
	let power_up_element = document.getElementById("gameCreatePowerStatus");
	let power_up_change_element = document.getElementById("btnStatusPowerUp");
	let team_left_element = document.getElementById("team1Player");
	let team_right_element = document.getElementById("team2Player");

	console.log("TEST")
	map_name_element.textContent = "Map " + map_id;

	if (power_up == "true")
	{
		power_up_element.textContent = "ON";
		power_up_element.style.color = "green";
		if (power_up_change_element)
			power_up_change_element.textContent = "ON";
	}
	else
	{
		power_up_element.textContent = "OFF";
		power_up_element.style.color = "red";
		if (power_up_change_element)
			power_up_change_element.textContent = "OFF";
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
	div.appendChild(pp);
	div.appendChild(username);

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

			for (let i = 0; i < list_invite.length; i++)
			{
				createInviteContact(invite_list_container, list_invite[i]);
			}
		})
		.catch(error => {
			console.log("erreur from getcanbeinvited :", error)
		});
}
