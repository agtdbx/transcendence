function getLocalTournamentStatus()
{
	let inter = setInterval(function () {
		if (webSocket != null && webSocket.readyState == WebSocket.OPEN)
		{
			webSocket.send(JSON.stringify({
				'type' : 'localTournament',
				'cmd' : 'getInfo'
			}));
			clearInterval(inter);
		}
		else
			console.log("wait connection");
	}, 10);
}


// Create local tournament page
function switchLocalTournamentPowerUp()
{
	webSocket.send(JSON.stringify({
		'type' : 'localTournament',
		'cmd' : 'modifyPowerUp'
	}));
}


function changeLocalTournamentMapId(mapId)
{
	webSocket.send(JSON.stringify({
		'type' : 'localTournament',
		'cmd' : 'modifyMapId',
		'mapId' : mapId
	}));
}


function LocalTournamentAddPlayer(nickname)
{
	webSocket.send(JSON.stringify({
		'type' : 'localTournament',
		'cmd' : 'addPlayer',
		'nickname' : nickname
	}));
}


function LocalTournamentRemovePlayer(nickname)
{
	webSocket.send(JSON.stringify({
		'type' : 'localTournament',
		'cmd' : 'removePlayer',
		'nickname' : nickname
	}));
}


function createLocalTournament()
{
	console.log("createLocalTournament");
	webSocket.send(JSON.stringify({
		'type' : 'localTournament',
		'cmd' : 'create'
	}));
}


function startLocalTournament()
{
	console.log("start tournament !!!");
	webSocket.send(JSON.stringify({
		'type' : 'localTournament',
		'cmd' : 'start'
	}));
}


function addLocalPlayerViewsTournament(player, div)
{
	let pp = document.createElement("img");
	pp.src = player[1];
	pp.style.width = "3em";
	pp.style.height = "3em";

	let nickname = document.createElement("p");
	nickname.textContent = player[2];
	nickname.style.color = "white";

	let playerDiv = document.createElement("div");
	playerDiv.style.display = "flex";
	playerDiv.style.flexDirection = "row";
	playerDiv.style.width = "100%";
	playerDiv.appendChild(pp);
	playerDiv.appendChild(nickname);
	playerDiv.onclick = function () {
		LocalTournamentRemovePlayer(player[2]);
	};

	div.appendChild(playerDiv);
}


function waitCreationLocalTournament(status, mapId, powerUp, listPlayers)
{
	let inter = setInterval(function () {
		if (pageInLoad == false)
		{
			updateCreationLocalTournament(status, mapId, powerUp, listPlayers);
			clearInterval(inter);
		}
		else
			console.log("wait");
	}, 10);
}


function updateCreationLocalTournament(status, mapId, powerUp, listPlayers)
{
	let mainButton = document.getElementById("btnTournamentCreate");
	let addPlayerForm = document.getElementById("addLocalPlayerForm");
	let allModiferDiv = document.getElementById("allModifierTournament");

	// Change button name and visibility with tournament status
	if (status == 0 || status == 3)
	{
		mainButton.textContent = "Create Tournament";
		mainButton.hidden = false;
		mainButton.onclick = function () {
			createLocalTournament();
		}
		addPlayerForm.hidden = true;
		allModiferDiv.hidden = true;
	}
	else if (status == 1)
	{
		mainButton.textContent = "Start Tournament";
		mainButton.hidden = false;
		mainButton.onclick = function () {
			startLocalTournament();
		}
		addPlayerForm.hidden = false;
		allModiferDiv.hidden = false;
	}
	else
	{
		mainButton.hidden = true;
		addPlayerForm.hidden = true;
		allModiferDiv.hidden = true;
	}

	// Hilight the map choose
	for (let i = 0; i < 5; i++)
	{
		let mapBtn = document.getElementById("btnMap" + i);

		if (i == mapId)
			mapBtn.classList = "btn-drg btn-map";
		else
			mapBtn.classList = "btn-drg-dark btn-map";
	}

	// Change power text
	let powerUpBtn = document.getElementById("btnStatusPowerUp");

	if (powerUp == "true")
		powerUpBtn.textContent = "ON";
	else
		powerUpBtn.textContent = "OFF";

	// Display all user
	let listPlayersDiv = document.getElementById("tournamentrect3");
	listPlayersDiv.innerHTML = "";
	for (let i = 0; i < listPlayers.length; i++)
	{
		addLocalPlayerViewsTournament(listPlayers[i], listPlayersDiv);
	}
}


// TOURNAMENT TREE
function getLocalTournamentTree()
{
	console.log('Get tree local tournament');

	let inter = setInterval(function () {
		if (webSocket != null && webSocket.readyState == WebSocket.OPEN)
		{
			webSocket.send(JSON.stringify({
				'type' : 'localTournament',
				'cmd' : 'getTournamentTree'
			}));
			clearInterval(inter);
		}
		else
		console.log("wait connection");
}, 10);
}

// NEXT MATCH
function getLocalTournamentNextMatch()
{
	console.log('Get next match tournament');

	let inter = setInterval(function () {
		if (webSocket != null && webSocket.readyState == WebSocket.OPEN)
		{
			webSocket.send(JSON.stringify({
				'type' : 'localTournament',
				'cmd' : 'nextMatch'
			}));
			clearInterval(inter);
		}
		else
			console.log("wait connection");
	}, 10);
}

// TOURNAMENT RESULT
function getLocalTournamentResult()
{
	console.log('Get result of tournament');

	let inter = setInterval(function () {
		if (webSocket != null && webSocket.readyState == WebSocket.OPEN)
		{
			webSocket.send(JSON.stringify({
				'type' : 'localTournament',
				'cmd' : 'winners'
			}));
			clearInterval(inter);
		}
		else
			console.log("wait connection");
	}, 10);
}

// Local tournament page
function applyLocalTournamentState(mapName, powerUp, listPlayers)
{
	let playersDiv = document.getElementById("UserList");

	if (playersDiv != null)
	{
		playersDiv.innerHTML = "";
		if (playersDiv != null)
		{
			for (let i = 0; i < listPlayers.length; i++)
			{
				addPlayerViewsTournament(listPlayers[i], playersDiv);
			}
		}
	}

	let powerUpP = document.getElementById("powerUpTournamentJoin");
	if (powerUpP != null)
	{
		if (powerUp == 'true')
			powerUpP.textContent = "Power up : on";
		else
			powerUpP.textContent = "Power up : off";
	}

	let mapP = document.getElementById("powerUpTournamentMap");
	if (mapP != null)
		mapP.textContent = "Map : " + mapName;
}
