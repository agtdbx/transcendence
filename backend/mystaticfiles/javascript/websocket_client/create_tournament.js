function goToCreateTournament()
{
	changePage('8');
	let inter = setInterval(function () {
		if (pageInLoad == false)
		{
			pageForTournamentStatus = "create";
			getTournamentStatus();
			clearInterval(inter);
		}
		else
			console.log("wait");
	}, 10);
}


function addPlayerViewsTournament(player, div)
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
	playerDiv.appendChild(pp);
	playerDiv.appendChild(nickname);

	div.appendChild(playerDiv);
}


function assignTournamentStatusOnCreatePage(status, mapId, powerUp, listPlayers)
{
	let mainButton = document.getElementById("btnTournamentCreate");
	let allModiferDiv = document.getElementById("allModifierTournament");

	// Change button name and visibility with tournament status
	if (status == 0 || status == 3)
	{
		mainButton.textContent = "Create Tournament";
		mainButton.hidden = false;
		mainButton.onclick = function () {
			createTournament();
		}
		allModiferDiv.hidden = true;
	}
	else if (status == 1)
	{
		mainButton.textContent = "Start Tournament";
		mainButton.hidden = false;
		mainButton.onclick = function () {
			startTournament();
		}
		allModiferDiv.hidden = false;
	}
	else
	{
		mainButton.hidden = true;
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
		addPlayerViewsTournament(listPlayers[i], listPlayersDiv);
	}
}


function switchTournamentPowerUp()
{
	webSocket.send(JSON.stringify({
		'type' : 'tournament',
		'cmd' : 'modifyPowerUp'
	}));
}


function changeTournamentMapId(mapId)
{
	webSocket.send(JSON.stringify({
		'type' : 'tournament',
		'cmd' : 'modifyMapId',
		'mapId' : mapId
	}));
}


function createTournament()
{
	console.log("createTournament");
	webSocket.send(JSON.stringify({
		'type' : 'tournament',
		'cmd' : 'create',
		'powerUp' : false ,
		'mapId' : 0
	}));
}


function startTournament()
{
	console.log("start tournament !!!");
	webSocket.send(JSON.stringify({
		'type' : 'tournament',
		'cmd' : 'start'
	}));
}
