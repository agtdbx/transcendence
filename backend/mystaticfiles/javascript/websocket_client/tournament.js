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
		quitBut.hidden = false;
		quitBut.onclick = function () {
			quitTournament();
		};
	}
	else
	{
		quitBut.hidden = true;
		quitBut.onclick = null;
	}

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
	if (powerUp == 'true')
		powerUpP.textContent = "Power up : on";
	else
		powerUpP.textContent = "Power up : off";

	let mapP = document.getElementById("powerUpTournamentMap");
	mapP.textContent = "Map : map " + mapId;

	if (state != 2)
		return ;
}


// TOURNAMENT TREE
function getTournamentTree()
{
	console.log('Get tree tournament');

	let inter = setInterval(function () {
		if (webSocket.readyState != WebSocket.CONNECTING)
		{
			webSocket.send(JSON.stringify({
				'type' : 'tournament',
				'cmd' : 'getTournamentTree'
			}));
			clearInterval(inter);
		}
		else
			console.log("wait connection");
	}, 10);
}


function waitTournamentTree(playersGrade)
{
	let inter = setInterval(function () {
		if (pageInLoad == false)
		{
			setTournamentTree(playersGrade);
			clearInterval(inter);
		}
		else
			console.log("wait");
	}, 10);
}


function setTournamentTree(playersGrade)
{
	console.log("TOURNAMENT TREE SET");

	let graphe = document.getElementById("graphe");

	if (graphe == null)
	{
		console.log("No graph found");
		return ;
	}

	let playerList = [];

	for (let i = 0; i < playersGrade.length; i++)
	{
		playerList.push({
			"grade" : playersGrade[i][1],
			"img": "https://static.wikia.nocookie.net/deeprockgalactic_gamepedia_en/images/c/c5/Mining_expedition_icon.png/revision/latest/scale-to-width-down/40?cb=20220313105613"
		});
	}
	// {
	// 	"grade":0,
	// 	"img": "https://static.wikia.nocookie.net/deeprockgalactic_gamepedia_en/images/c/c5/Mining_expedition_icon.png/revision/latest/scale-to-width-down/40?cb=20220313105613"
	// },
	// {
	// 	"grade":0,
	// 	"img": "https://static.wikia.nocookie.net/deeprockgalactic_gamepedia_en/images/8/89/Unknown_lightgray.png/revision/latest/scale-to-width-down/250?cb=20210416205542"
	// },
	// {
	// 	"grade":0,
	// 	"img": "https://static.wikia.nocookie.net/deeprockgalactic_gamepedia_en/images/8/89/Unknown_lightgray.png/revision/latest/scale-to-width-down/250?cb=20210416205542"
	// },
	// {
	// 	"grade":0,
	// 	"img": "https://static.wikia.nocookie.net/deeprockgalactic_gamepedia_en/images/8/89/Unknown_lightgray.png/revision/latest/scale-to-width-down/250?cb=20210416205542"
	// },
	// {
	// 	"grade":0,
	// 	"img": "https://static.wikia.nocookie.net/deeprockgalactic_gamepedia_en/images/8/89/Unknown_lightgray.png/revision/latest/scale-to-width-down/250?cb=20210416205542"
	// },
	// {
	// 	"grade":0,
	// 	"img": "https://static.wikia.nocookie.net/deeprockgalactic_gamepedia_en/images/8/89/Unknown_lightgray.png/revision/latest/scale-to-width-down/250?cb=20210416205542"
	// },
	// {
	// 	"grade":0,
	// 	"img": "https://static.wikia.nocookie.net/deeprockgalactic_gamepedia_en/images/8/89/Unknown_lightgray.png/revision/latest/scale-to-width-down/250?cb=20210416205542"
	// },
	// {
	// 	"grade":0,
	// 	"img": "https://static.wikia.nocookie.net/deeprockgalactic_gamepedia_en/images/8/89/Unknown_lightgray.png/revision/latest/scale-to-width-down/250?cb=20210416205542"
	// }

	// createTournamentTree(graphe, playerList);
}


// NEXT MATCH
function getTournamentNextMatch()
{
	console.log('Get next match tournament');

	let inter = setInterval(function () {
		if (webSocket.readyState != WebSocket.CONNECTING)
		{
			webSocket.send(JSON.stringify({
				'type' : 'tournament',
				'cmd' : 'nextMatch'
			}));
			clearInterval(inter);
		}
		else
			console.log("wait connection");
	}, 10);
}


function waitTournamentNextMatch(match)
{
	let inter = setInterval(function () {
		if (pageInLoad == false)
		{
			setTournamentNextMatch(match);
			clearInterval(inter);
		}
		else
			console.log("wait");
	}, 10);
}

function setTournamentNextMatch(match)
{
	console.log("NEXT MATCH SET");

	if (match == null)
	{
		console.log("THERE IS NO NEXT MATCH");
		return ;
	}

	let p1Div = document.getElementById("tournamentPlayer1");
	let p2Div = document.getElementById("tournamentPlayer2");

	p1Div.innerHTML = "";
	if (match[0] != "null")
		addPlayerViewsTournament(match[0], p1Div);
	p2Div.innerHTML = "";
	if (match[1] != "null")
		addPlayerViewsTournament(match[1], p1Div);
}


// MY NEXT MATCH
function getTournamentMyNextMatch()
{
	console.log('Get my next match tournament');

	let inter = setInterval(function () {
		if (webSocket.readyState != WebSocket.CONNECTING)
		{
			webSocket.send(JSON.stringify({
				'type' : 'tournament',
				'cmd' : 'myNextMatch'
			}));
			clearInterval(inter);
		}
		else
			console.log("wait connection");
	}, 10);
}

function waitTournamentMyNextMatch(match)
{
	let inter = setInterval(function () {
		if (pageInLoad == false)
		{
			setTournamentMyNextMatch(match);
			clearInterval(inter);
		}
		else
			console.log("wait");
	}, 10);
}

function setTournamentMyNextMatch(match)
{
	console.log("MY NEXT MATCH SET :", match, typeof(match));

	if (match == "null")
	{
		console.log("THERE IS NO NEXT MATCH");
		return ;
	}

	let p1Div = document.getElementById("tournamentPlayer3");
	let p2Div = document.getElementById("tournamentPlayer4");

	if (p1Div == "null" || p2Div == "null")
	{
		console.log("NO MY NEXT MATCH HERE");
		return ;
	}


	p1Div.innerHTML = "";
	if (match[0] != "null")
		addPlayerViewsTournament(match[0], p1Div);
	p2Div.innerHTML = "";
	if (match[1] != "null")
		addPlayerViewsTournament(match[1], p1Div);
}


// TOURNAMENT RESULT
function getTournamentResult()
{
	console.log('Get result of tournament');

	let inter = setInterval(function () {
		if (webSocket.readyState != WebSocket.CONNECTING)
		{
			webSocket.send(JSON.stringify({
				'type' : 'tournament',
				'cmd' : 'winners'
			}));
			clearInterval(inter);
		}
		else
			console.log("wait connection");
	}, 10);
}

function waitTournamentResult(winner, second, third)
{
	let inter = setInterval(function () {
		if (pageInLoad == false)
		{
			setTournamentResult(winner, second, third);
			clearInterval(inter);
		}
		else
			console.log("wait");
	}, 10);
}

function setTournamentResult(winner, second, third)
{
	console.log("TOURNAMENT WINNERS SET");

	let winnerPP = document.getElementById("podiumPp1");
	winnerPP.src = winner[1];
	winnerPP.style.width = "100%";

	let winnerNickname = document.getElementById("usernamePodium1");
	winnerNickname.textContent = winner[2];

	let secondPP = document.getElementById("podiumPp2");
	secondPP.src = second[1];
	secondPP.style.width = "100%";

	let secondNickname = document.getElementById("usernamePodium2");
	secondNickname.textContent = second[2];

	let thirdPP = document.getElementById("podiumPp3");
	thirdPP.src = third[1];
	thirdPP.style.width = "100%";

	let thirdNickname = document.getElementById("usernamePodium3");
	thirdNickname.textContent = third[2];
}
