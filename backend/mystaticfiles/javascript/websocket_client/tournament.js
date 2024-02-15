let pageForTournamentStatus = null;

function getTournamentStatus()
{
	let inter = setInterval(function () {
		if (webSocket.readyState != WebSocket.CONNECTING)
		{
			webSocket.send(JSON.stringify({
				'type' : 'tournament',
				'cmd' : 'getInfo'
			}));
			clearInterval(inter);
		}
		else
			console.log("wait connection");
	}, 10);
}


function manageMainpageButton(status, mapId, powerUp, listPlayers, youInTournament)
{
	let inter = setInterval(function () {
		if (pageInLoad == false)
		{
			clearInterval(inter);

			let butJoinTournament = document.getElementById("mainBtnJoin");

			butJoinTournament.hidden = false;
			if (status == 0)
				butJoinTournament.hidden = true;
			else if (status == 1)
			{
				if (youInTournament == "true")
				{
					butJoinTournament.textContent = "View";
					butJoinTournament.onclick = function () {
						changePage("71");
						waitTournamentState(status, mapId, powerUp, listPlayers, youInTournament);
					}
				}
				else if (listPlayers.length == 8)
				{
					butJoinTournament.textContent = "Spectate";
					butJoinTournament.onclick = function () {
						changePage("72");
						waitTournamentState(status, mapId, powerUp, listPlayers, youInTournament);
					}
				}
				else
				{
					butJoinTournament.textContent = "Register";
					butJoinTournament.onclick = function () {
						changePage("7");
					}
				}
			}
			else if (status == 2)
				if (youInTournament == "true")
				{
					butJoinTournament.textContent = "View";
					butJoinTournament.onclick = function () {
						changePage("71");
						waitTournamentState(status, mapId, powerUp, listPlayers, youInTournament);
					}
				}
				else
				{
					butJoinTournament.textContent = "Spectate";
					butJoinTournament.onclick = function () {
						changePage("72");
						waitTournamentState(status, mapId, powerUp, listPlayers, youInTournament);
					}
				}
			else
			{
				butJoinTournament.textContent = "Result";
				butJoinTournament.onclick = function () {
					changePage("73");
				}
			}

			let butCreateTournament = document.getElementById("mainBtnAdmin");

			if (butCreateTournament == null)
				return ;

			butCreateTournament.hidden = false;
			if (status == 0 || status == 3)
				butCreateTournament.textContent = "Create tournament";
			else if (status == 1)
				butCreateTournament.textContent = "Modify tournament";
			else
				butCreateTournament.hidden = true;
		}
		else
			console.log("wait");
	}, 10);
}


function joinTournament(nickname)
{
	console.log('Join tournament with nickname', nickname);
	webSocket.send(JSON.stringify({
		'type' : 'tournament',
		'cmd' : 'join',
		'nickname' : nickname
	}));
}


function quitTournament()
{
	console.log('Quick tournament');
	webSocket.send(JSON.stringify({
		'type' : 'tournament',
		'cmd' : 'quit'
	}));
}


function getTournamentTree()
{
	console.log('Get tree tournament');
	webSocket.send(JSON.stringify({
		'type' : 'tournament',
		'cmd' : 'getTournamentTree'
	}));
}


function waitTournamentState(state, mapId, powerUp, listPlayers, youInTournament)
{
	getTournamentTree();
	let inter = setInterval(function () {
		if (pageInLoad == false)
		{
			applyTournamentState(state, mapId, powerUp, listPlayers, youInTournament);
			clearInterval(inter);
		}
		else
			console.log("wait");
	}, 10);
}


function applyTournamentState(state, mapId, powerUp, listPlayers, youInTournament)
{
	let quitBut = document.getElementById("btnTournamentQuit");

	if (state == 1 && youInTournament == 'true')
	{
		quitBut.textContent = "Quit";
		quitBut.onclick = function () {
			quitTournament();
		};
	}
	else
	{
		quitBut.textContent = "Return";
		quitBut.onclick = function () {
			changePage('3');
		};
	}

	let playersDiv = document.getElementById("UserList");

	if (playersDiv != null)
	{
		for (let i = 0; i < listPlayers.length; i++)
		{
			addPlayerViewsTournament(listPlayers[i], playersDiv);
		}
	}

	let powerUpP = document.getElementById("powerUpTournamentJoin");
	if (powerUp == 'true')
		powerUpP.textContent = "Power up : on";
	else
		powerUpP.textContent = "Power up : off";

	let mapP = document.getElementById("powerUpTournamentMap");
	mapP.textContent = "Map : map " + mapId;

	if (state != 2)
		return ;

	// Get next match !
}


function waitTournamentTree()
{
	getTournamentTree();
	let inter = setInterval(function () {
		if (pageInLoad == false)
		{
			setTournamentTree();
			clearInterval(inter);
		}
		else
			console.log("wait");
	}, 10);
}


function setTournamentTree()
{

}
